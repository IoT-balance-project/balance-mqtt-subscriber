---
title: "IoT balance: Loading raw data example"
---

```r
library(dplyr)
library(fs)
library(readr)
```

# Load CSV data

This is an example notebook that loads all the balance data.

```r
DATA_DIR <- "X:\\global_plant_ecology\\data\\balance"
```

Get the path of all CSV files

```r
paths <- fs::dir_ls(DATA_DIR, recurse = TRUE, glob = "*.csv")
```

Define a function to parse the raw CSV data.

```r
load_csv <- function(path) {
  # Parse the CSV file
  data <- readr::read_csv(path, col_names = FALSE, col_types = readr::cols(
    X1 = readr::col_datetime(format = ""),
    X2 = readr::col_character()
    )
  )
  # Convert the subdirectory to the MQTT topic
  data$topic <- fs::path_ext_remove(fs::path_rel(path, DATA_DIR))
  return (data)
}
```

Load the data by iterating over all the CSV files.

```r
data <- dplyr::bind_rows(lapply(paths, load_csv))
```

Show the data

```r
head(data)
```
