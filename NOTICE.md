# Data And Asset Notice

AudienceKit
Copyright 2026 Luca Fiaschi

The Apache License 2.0 covers the AudienceKit source code.

## Bundled GSS 2024 Public-Use Data

`audiencekit/data/2024_stata.zip` is the public GSS 2024 cross-sectional Stata
bundle downloaded from NORC at the University of Chicago. It includes
`GSS2024.dta` and NORC's Release 3 documentation.

AudienceKit uses this file as the default panel source for examples and smoke
tests. For trend work or larger historical sampling frames, download the current
GSS 1972-2024 cumulative file from NORC and prepare your own panel with
`audiencekit.gss.load_gss` or `scripts/extract_panel.py`.

Recommended GSS citation:

> Davern, Michael; Bautista, Rene; Freese, Jeremy; Herd, Pamela; and Morgan,
> Stephen L. General Social Survey 1972-2024. [Machine-readable data file].
> Principal Investigator, Michael Davern; Co-Principal Investigators, Rene
> Bautista, Jeremy Freese, Pamela Herd, and Stephen L. Morgan. NORC ed.
> Chicago, 2026. 1 datafile and 1 codebook (2024 Release 3).

Review NORC's data access terms before redistributing derived data:
https://gss.norc.org/get-the-data.html

## Ferrari Luce Example

The Ferrari Luce example is an educational synthetic research case study.
Ferrari and Prancing Horse marks belong to their owners. Example stimuli are
not part of the AudienceKit software license. Replace them with your own
properly licensed assets before using the example for public, commercial, or
redistributed work.
