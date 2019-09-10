# ddg-retriever

Retrieve search results from [Duck Duck Go](https://duckduckgo.com/).

# Setup

Python 3 is required. The dependencies are specified in `requirements.txt`.
To install those dependencies execute:

    pip3 install -r requirements.txt

**Optional:** Setup virtual environment with [pyenv](https://github.com/pyenv/pyenv) 
and [virtualenv](https://github.com/pyenv/pyenv-virtualenv) before executing the above command:

    pyenv install 3.7.4
    pyenv virtualenv 3.7.4 ddg-retriever_3.7.4
    pyenv activate ddg-retriever_3.7.4
    
    pip3 install --upgrade pip

# Usage

Basic usage:

    python3 ddg-retriever.py -c <path_to_config_file>

# Configuration

The configuration in stored in a [configuration file](config.ini):

    [DEFAULT]
    InputFile = input/queries.csv
    OutputDirectory = output
    Delimiter = ,
    ExactMatches = True
    RemoveSpecialCharacters = True
    MaxResults = 25
    MinWait = 500
    MaxWait = 2000
    DetectLanguages = True

As input, the tool expects a CSV file with one column named `query`.
An exemplary input file can be found [here](input/queries.csv):

| query |
|-------|
| Interrupt handler |
| SQL injection |
| Plug-in (computing) |
| Rule of three (C++ programming) |
| ...   |

Alternatively, a list of search results previously exported with this tool can be used as input file to detect the
languages of the retrieved snippets.
To retrieve the search results as exact matches and automatically detect the languages of the retrieved snippets
for the configured queries, you just need to run the following command:

    python3 ddg-retriever.py -c config.ini

The tool logs the retrieval process:

    2019-09-08 12:59:16,391 ddg-retriever_logger INFO: Checking input format in input/queries.csv...
    2019-09-08 12:59:16,391 ddg-retriever_logger INFO: Input file contains only queries, retrieving search results...
    2019-09-08 12:59:16,391 ddg-retriever_logger INFO: Reading search queries from input/queries.csv...
    2019-09-08 12:59:16,392 ddg-retriever_logger INFO: 4 search queries have been imported.
    2019-09-08 12:59:17,259 ddg-retriever_logger INFO: Successfully retrieved search results for query: "Interrupt handler"
    2019-09-08 12:59:17,268 ddg-retriever_logger INFO: Successfully parsed result list for query: "Interrupt handler"
    2019-09-08 12:59:17,269 ddg-retriever_logger INFO: Detecting snippet languages...
    2019-09-08 12:59:19,714 ddg-retriever_logger INFO: Successfully retrieved search results for query: "SQL injection"
    2019-09-08 12:59:19,727 ddg-retriever_logger INFO: Successfully parsed result list for query: "SQL injection"
    2019-09-08 12:59:19,727 ddg-retriever_logger INFO: Detecting snippet languages...
    2019-09-08 12:59:22,032 ddg-retriever_logger INFO: Successfully retrieved search results for query: "Plug-in" "computing"
    2019-09-08 12:59:22,049 ddg-retriever_logger INFO: Successfully parsed result list for query: "Plug-in" "computing"
    2019-09-08 12:59:22,050 ddg-retriever_logger INFO: Detecting snippet languages...
    2019-09-08 12:59:23,009 ddg-retriever_logger INFO: Successfully retrieved search results for query: "Rule of three" "C++ programming"
    2019-09-08 12:59:23,018 ddg-retriever_logger INFO: Successfully parsed result list for query: "Rule of three" "C++ programming"
    2019-09-08 12:59:23,019 ddg-retriever_logger INFO: Detecting snippet languages...
    2019-09-08 12:59:23,127 ddg-retriever_logger INFO: Exporting search results to output/queries.csv...
    2019-09-08 12:59:23,128 ddg-retriever_logger INFO: 99 search results have been exported.

And writes the [retrieved data](output/queries.csv) to the configured output directory:

| query               | rank | language | url                                                                             | title                         | snippet                                                                                                                                                                                                                                                                                                                                                                                                     |
|---------------------|------|----------|---------------------------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| "Interrupt handler" |   1  | en       | https://en.wikipedia.org/wiki/Interrupt_handler                                 | Interrupt handler - Wikipedia | In computer systems programming, an interrupt handler, also known as an interrupt service routine or ISR, is a special block of code associated with a specific interrupt condition. Interrupt handlers are initiated by hardware interrupts, software interrupt instructions, or software exceptions, and are used for implementing device drivers or transitions between protected modes of operation ... |
| "Interrupt handler" |   2  | en       | https://www3.nd.edu/~lemmon/courses/ee224/web-manual/web-manual/lab7/node5.html | What is an Interrupt Handler? | What is an Interrupt Handler? Let's consider a program that the MicroStamp11 is executing. A program is a list of instructions that the micro-controller executes in a sequential manner. A hardware event is something special that happens in the micro-controller's hardware. An example of such an event is the RESET that occurs when pin 9 on the ...                                                 |
| ...                 | ...  | ...      | ...                                                                             | ...                           | ...                                                                                                                                                                                                                                                                                                                                                                                                         |

If `RemoveSpecialCharacters` is `True`, the tool splits the search query along certain special characters (see `Query.special_character_regex`):

| query                 | rank | language | url                                                                             | title                           | snippet                                                                                                                                                                                                                                                                                                                                                                                                  |
|-----------------------|------|----------|---------------------------------------------------------------------------------|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ...                   | ...  | ...      | ...                                                                             | ...                             | ...                                                                                                                                                                                                                                                                                                                                                                                                      |
| "Plug-in" "computing" | 1    | en       | https://en.wikipedia.org/wiki/Plug-in_%28computing%29                           | Plug-in (computing) - Wikipedia | In computing, a plug-in (or plugin, add-in, addin, add-on, or addon) is a software component that adds a specific feature to an existing computer program. When a program supports plug-ins, it enables customization.                                                                                                                                                                                   |
| ...                   | ...  | ...      | ...                                                                             | ...                             | ...                                                                                                                                                                                                                                                                                                                                                                                                      |
