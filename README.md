# Globalhealth 50/50 - COVID-19 Data tracker

Global Health 50/50 is an independent, evidence-driven initiative to advance action and accountability for gender equality in global health. The collective and it's work can only be deemed a success when global health policy and organisational decision-making puts a gender lens, gender equality and health equity at the core of all it does.


From the first reports of the novel coronavirus, COVID-19, there has been consistent evidence of a gendered impact on health outcomes.
This tool to automates data fetching for COVID-19 by country, including gender disparities in reporting, testing, and outcomes.

<!-- ## Project Features

* [covid_data_tracker](http://GH5050_COVID_Data_Tracker.readthedocs.io/) -->


## Usage

covid_data_tracker provides a command line application `covidtracker`:

```
covidtracker download --help
Usage: covidtracker download [OPTIONS]

  Download country level statistics

Options:
  -c, --country TEXT  Select a country.
  -A, --all TEXT      Select all countries. (overrides --country)
  --help              Show this message and exit.
 ```

```
$ covidtracker
Usage: covidtracker [OPTIONS] COMMAND [ARGS]...

 Run covidtracker.

Options:
 -v, --verbose  Enable verbose output.
 --help         Show this message and exit.

Commands:
 download  Download country level statistics
 info      Get country level information on sources and download strategy
 version   Get the library version.
```

## Getting Started

The project's documentation contains a section to help you
[get started](https://GH5050_COVID_Data_Tracker.readthedocs.io/en/latest/getting_started.html) as a developer or user of the library.


## TODO

- [ ] Pull from archive data (all or date specific)
- [ ] Provide information on countries (sources, update frequency, etc)
- [ ] A plugin registration strategy that uses metaclasses


## Development Guidelines

We encourage people to participate in developing country plugins and reviewing the reliability of existing plugins.  If you are interested in contributing, please create an issue using the source checklist template (this prevents effort duplication).


## Resources

* [Global Health 50/50](https://globalhealth5050.org/) is an organization that promotes gender equality in global health
* [Global Health 50/50 COVID resources and information](https://globalhealth5050.org/)
* [Granular.ai](https://granular.ai) is helping to develop this tool


## Authors

* **Sid Gupta** - *Initial work* - [github](https://github.com/granularai)

See also the list of [contributors](https://github.com/granularai/covid_data_tracker/contributors) who participated in this project.

## License

MIT License

Copyright (c) Granular.ai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
