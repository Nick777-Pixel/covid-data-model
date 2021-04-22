import datetime
from typing import List
from typing import Optional
from typing import Tuple

import pydantic
import structlog
from covidactnow.datapublic.common_fields import CommonFields
from covidactnow.datapublic.common_fields import PdFields
import pandas as pd

from libs.datasets import taglib
from libs.datasets import timeseries
from libs.pipeline import RegionMaskOrRegion

_logger = structlog.getLogger()


# The manual filter config is defined with pydantic instead of standard dataclasses to get support
# for parsing from json, automatic conversion of fields to the expected type and avoiding the
# dreaded "TypeError: non-default argument ...". pydantic reserves the field name 'fields'.


class Filter(pydantic.BaseModel):
    regions_included: List[RegionMaskOrRegion]
    regions_excluded: Optional[List[RegionMaskOrRegion]] = None
    fields_included: List[CommonFields]
    start_date: Optional[datetime.date] = None
    drop_observations: bool
    internal_note: str
    # public_note may be any empty string
    public_note: str

    @property
    def tag(self) -> taglib.TagInTimeseries:
        return taglib.KnownIssue(date=self.start_date, disclaimer=self.public_note)

    # From https://github.com/samuelcolvin/pydantic/issues/568 ... pylint: disable=no-self-argument
    @pydantic.root_validator()
    def check(cls, values):
        if not values["drop_observations"]:
            if values["public_note"] == "":
                raise ValueError(
                    "Filter doesn't drop observations or add a public_note. What does it do?"
                )
            if values["start_date"]:
                raise ValueError(
                    "Filter including start_date without dropping observations "
                    "doesn't make sense."
                )
        return values


class Config(pydantic.BaseModel):
    filters: List[Filter]


CONFIG = Config(filters=[])


def _partition_by_fields(
    ts_in: pd.DataFrame, fields: List[CommonFields]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Partitions a DataFrame with timeseries wide dates into two: fields and others."""
    timeseries.check_timeseries_wide_dates_structure(ts_in)
    mask_selected_fields = ts_in.index.get_level_values(PdFields.VARIABLE).isin(fields)
    ts_selected_fields = ts_in.loc[mask_selected_fields]
    ts_not_selected_fields = ts_in.loc[~mask_selected_fields]
    return ts_selected_fields, ts_not_selected_fields


def _filter_by_date(
    ts_in: pd.DataFrame, *, drop_start_date: datetime.date
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Removes observations from specified dates, returning the modified timeseries and
    unmodified timeseries in separate DataFrame objects."""
    timeseries.check_timeseries_wide_dates_structure(ts_in)
    start_date = pd.to_datetime(drop_start_date)
    obsv_selected = ts_in.loc[:, ts_in.columns >= start_date]
    mask_has_real_value_to_drop = obsv_selected.notna().any(1)
    ts_to_filter = ts_in.loc[mask_has_real_value_to_drop]
    ts_no_real_values_to_drop = ts_in.loc[~mask_has_real_value_to_drop]
    ts_filtered = ts_to_filter.loc[:, ts_to_filter.columns < start_date]
    return ts_filtered, ts_no_real_values_to_drop


def drop_observations(
    dataset: timeseries.MultiRegionDataset, filter_: Filter
) -> timeseries.MultiRegionDataset:
    """Drops observations according to `filter_` from every region in `dataset`."""
    assert filter_.drop_observations

    # wide-dates DataFrames that will be concat-ed to produce the result MultiRegionDataset.
    ts_results = []
    ts_selected_fields, ts_not_selected_fields = _partition_by_fields(
        dataset.timeseries_bucketed_wide_dates, filter_.fields_included
    )
    ts_results.append(ts_not_selected_fields)

    ts_filtered, ts_no_real_values_to_drop = _filter_by_date(
        ts_selected_fields, drop_start_date=filter_.start_date
    )
    ts_results.append(ts_filtered)
    ts_results.append(ts_no_real_values_to_drop)
    index_to_tag = ts_filtered.index

    return dataset.replace_timeseries_wide_dates(ts_results).add_tag_to_subset(
        filter_.tag, index_to_tag
    )


def run(
    dataset: timeseries.MultiRegionDataset, config: Config = CONFIG
) -> timeseries.MultiRegionDataset:
    for filter_ in config.filters:
        filtered_dataset, passed_dataset = dataset.partition_by_region(
            filter_.regions_included, exclude=filter_.regions_excluded
        )
        if filtered_dataset.location_ids.empty:
            # TODO(tom): Find a cleaner way to refer to a filter in logs.
            _logger.info("No locations matched", regions=str(filter_.regions_included))
            continue
        filtered_dataset = drop_observations(filtered_dataset, filter_)

        dataset = filtered_dataset.append_regions(passed_dataset)

    return dataset
