from covidactnow.datapublic import common_df
from covidactnow.datapublic.common_fields import CommonFields
from libs.datasets import data_source
from libs.datasets import dataset_utils
from libs.datasets.timeseries import TimeseriesDataset


class NYTimesDataset(data_source.DataSource):
    SOURCE_NAME = "NYTimes"

    DATA_PATH = "data/cases-nytimes/timeseries-common.csv"

    HAS_AGGREGATED_NYC_BOROUGH = True

    INDEX_FIELD_MAP = {f: f for f in TimeseriesDataset.INDEX_FIELDS}

    @classmethod
    def local(cls):
        data_root = dataset_utils.LOCAL_PUBLIC_DATA_PATH
        input_path = data_root / cls.DATA_PATH
        data = common_df.read_csv(input_path).reset_index()

        # Extra columns that we don't need and cause issues with aggregation.
        data = data.drop([CommonFields.COUNTY, CommonFields.STATE_FULL_NAME], axis=1)

        return cls(data)
