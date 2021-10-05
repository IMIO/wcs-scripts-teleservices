# Changelog
All notable changes to this project will be documented in this file.

## [0.0.35] - 15/06/2021 -
### Changed
  - [dmshd] : [INFRA-4003] [TELE-1119] add -k to avoid SSL error following the Infra advice about that

## [0.0.29] - 15/06/2021 -
### Changed
  - [nhi] : fix script to compute for bloc field

## [0.0.28] - 15/06/2021 -
### Changed
  - [mbr] : add script to compute price for bloc fields

## [0.0.27] - 11/05/2021 -
### Changed
  - [nhi] : filter user's demands on status id

## [0.0.26] - 10/05/2021 -
### Changed
  - [nhi] : return exception when it occurs when closing plains
  - [nhi] : use site_url instead of eservices_url

## [0.0.25] - 10/05/2021 -
### Changed
  - [nhi] : do not loop on demands without status

## [0.0.24] - 19/03/2021 -
### Changed
  - [nhi] : add script to get monday's date of a given week

## [0.0.23] - 23/11/2020 -
### Changed
  - [nse, nhi] : add fields_bloc to calculate the total from datasource additional key

## [0.0.22] - 14/09/2020 -
### Changed
  - [nse, nhi] : use range instead of xrange in town.py because xrange is deprecated in python 3
  - [nse, nhi] : initiate changelog
