"""
Module to specify columns in output csvs.

Changing the column ordering breaks many of our users who rely on column indices
to reference in excel and google sheets.  The timeseries and summary csvs use these
to determine column ordering.  Recommended to be append only.
"""

SUMMARY_ORDER = [
    "fips",
    "country",
    "state",
    "county",
    "level",
    "lat",
    "locationId",
    "long",
    "population",
    "metrics.testPositivityRatio",
    "metrics.testPositivityRatioDetails.source",
    "metrics.caseDensity",
    "metrics.contactTracerCapacityRatio",
    "metrics.infectionRate",
    "metrics.infectionRateCI90",
    # UPDATE(2021/09/14): ICU Headroom columns have been removed from the API and replaced with
    # "unused" columns.
    "unused1",
    "unused2",
    "unused3",
    "unused4",
    "unused5",
    "metrics.icuCapacityRatio",
    "riskLevels.overall",
    "riskLevels.testPositivityRatio",
    "riskLevels.caseDensity",
    "riskLevels.contactTracerCapacityRatio",
    "riskLevels.infectionRate",
    # UPDATE(2021/09/14): ICU Headroom columns have been removed from the API and replaced with
    # "unused" columns.
    "unused6",
    "riskLevels.icuCapacityRatio",
    "actuals.cases",
    "actuals.deaths",
    "actuals.positiveTests",
    "actuals.negativeTests",
    "actuals.contactTracers",
    "actuals.hospitalBeds.capacity",
    "actuals.hospitalBeds.currentUsageTotal",
    "actuals.hospitalBeds.currentUsageCovid",
    # UPDATE(2021/09/14): Typical Usage columns have been removed from the API and replaced with
    # "unused" columns.
    "unused7",
    "actuals.icuBeds.capacity",
    "actuals.icuBeds.currentUsageTotal",
    "actuals.icuBeds.currentUsageCovid",
    # UPDATE(2021/09/14): Typical Usage columns have been removed from the API and replaced with
    # "unused" columns.
    "unused8",
    "actuals.newCases",
    "actuals.vaccinesDistributed",
    "actuals.vaccinationsInitiated",
    "actuals.vaccinationsCompleted",
    "lastUpdatedDate",
    "url",
    "metrics.vaccinationsInitiatedRatio",
    "metrics.vaccinationsCompletedRatio",
    "actuals.newDeaths",
    "actuals.vaccinesAdministered",
    "cdcTransmissionLevel",
]

# Due to an inconsistency with how we previously were generating column names,
# state files had a different set of columns (that including headroom details). To prevent
# breaking changes, summary order with no headroom details is included here for County,
# metro, and place summary files.
SUMMARY_ORDER_NO_HEADROOM_DETAILS = [
    "fips",
    "country",
    "state",
    "county",
    "level",
    "lat",
    "locationId",
    "long",
    "population",
    "metrics.testPositivityRatio",
    "metrics.testPositivityRatioDetails.source",
    "metrics.caseDensity",
    "metrics.contactTracerCapacityRatio",
    "metrics.infectionRate",
    "metrics.infectionRateCI90",
    # UPDATE(2021/09/14): ICU Headroom columns have been removed from the API and replaced with
    # "unused" columns.
    "unused1",
    "unused2",
    "metrics.icuCapacityRatio",
    "riskLevels.overall",
    "riskLevels.testPositivityRatio",
    "riskLevels.caseDensity",
    "riskLevels.contactTracerCapacityRatio",
    "riskLevels.infectionRate",
    # UPDATE(2021/09/14): ICU Headroom columns have been removed from the API and replaced with
    # "unused" columns.
    "unused3",
    "riskLevels.icuCapacityRatio",
    "actuals.cases",
    "actuals.deaths",
    "actuals.positiveTests",
    "actuals.negativeTests",
    "actuals.contactTracers",
    "actuals.hospitalBeds.capacity",
    "actuals.hospitalBeds.currentUsageTotal",
    "actuals.hospitalBeds.currentUsageCovid",
    # UPDATE(2021/09/14): Typical usage columns have been removed from the API and replaced with
    # "unused" columns.
    "unused4",
    "actuals.icuBeds.capacity",
    "actuals.icuBeds.currentUsageTotal",
    "actuals.icuBeds.currentUsageCovid",
    # UPDATE(2021/09/14): Typical usage columns have been removed from the API and replaced with
    # "unused" columns.
    "unused5",
    "actuals.newCases",
    "actuals.vaccinesDistributed",
    "actuals.vaccinationsInitiated",
    "actuals.vaccinationsCompleted",
    "lastUpdatedDate",
    "url",
    "metrics.vaccinationsInitiatedRatio",
    "metrics.vaccinationsCompletedRatio",
    "actuals.newDeaths",
    "actuals.vaccinesAdministered",
    "cdcTransmissionLevel",
]


TIMESERIES_ORDER = [
    "date",
    "country",
    "state",
    "county",
    "fips",
    "lat",
    "long",
    "locationId",
    "actuals.cases",
    "actuals.deaths",
    "actuals.positiveTests",
    "actuals.negativeTests",
    "actuals.contactTracers",
    "actuals.hospitalBeds.capacity",
    "actuals.hospitalBeds.currentUsageTotal",
    "actuals.hospitalBeds.currentUsageCovid",
    # UPDATE(2021/09/14): Typical usage columns have been removed from the API and replaced with
    # "unused" columns.
    "unused1",
    "actuals.icuBeds.capacity",
    "actuals.icuBeds.currentUsageTotal",
    "actuals.icuBeds.currentUsageCovid",
    # UPDATE(2021/09/14): Typical usage columns have been removed from the API and replaced with
    # "unused" columns.
    "unused2",
    "actuals.newCases",
    "actuals.vaccinesDistributed",
    "actuals.vaccinationsInitiated",
    "actuals.vaccinationsCompleted",
    "metrics.testPositivityRatio",
    "metrics.testPositivityRatioDetails",
    "metrics.caseDensity",
    "metrics.contactTracerCapacityRatio",
    "metrics.infectionRate",
    "metrics.infectionRateCI90",
    # UPDATE(2021/09/14): ICU Headroom columns have been removed from the API and replaced with
    # "unused" columns.
    "unused3",
    "unused4",
    "metrics.icuCapacityRatio",
    "riskLevels.overall",
    "metrics.vaccinationsInitiatedRatio",
    "metrics.vaccinationsCompletedRatio",
    "actuals.newDeaths",
    "actuals.vaccinesAdministered",
    "riskLevels.caseDensity",
    "cdcTransmissionLevel",
]
