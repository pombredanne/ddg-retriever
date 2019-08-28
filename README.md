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
    MaxResults = 25
    MinWait = 500
    MaxWait = 2000

As input, the tool expects a CSV file with one column named `query`.
An exemplary input file can be found [here](input/queries.csv):

| query |
|-------|
| interrupt handler |
| sql injection|
| ...   |

To retrieve the search results as exact matches for the configured queries, you just need to run the following command:

    python3 ddg-retriever.py -c config.ini

The tool logs the retrieval process:

    2019-08-28 14:27:27,484 ddg-retriever_logger INFO: Reading search queries from input/queries.csv...
    2019-08-28 14:27:27,491 ddg-retriever_logger INFO: 2 search queries have been imported.
    2019-08-28 14:27:28,843 ddg-retriever_logger INFO: Successfully retrieved search results for query: "interrupt handler"
    2019-08-28 14:27:28,847 ddg-retriever_logger INFO: Successfully parsed result list for query: "interrupt handler"
    2019-08-28 14:27:29,694 ddg-retriever_logger INFO: Successfully retrieved search results for query: "sql injection"
    2019-08-28 14:27:29,701 ddg-retriever_logger INFO: Successfully parsed result list for query: "sql injection"
    2019-08-28 14:27:29,708 ddg-retriever_logger INFO: Exporting search results to output/queries.csv...
    2019-08-28 14:27:29,709 ddg-retriever_logger INFO: 50 search results have been exported.

And writes the [retrieved data](output/queries.csv) to the configured output directory:

| query               | rank | url                                                                             | title                         | snippet                                                                                                                                                                                                                                                                                                                                                                                                     |
|---------------------|------|---------------------------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| "interrupt handler" |   1  | https://en.wikipedia.org/wiki/Interrupt_handler                                 | Interrupt handler - Wikipedia | In computer systems programming, an interrupt handler, also known as an interrupt service routine or ISR, is a special block of code associated with a specific interrupt condition. Interrupt handlers are initiated by hardware interrupts, software interrupt instructions, or software exceptions, and are used for implementing device drivers or transitions between protected modes of operation ... |
| "interrupt handler" |   2  | https://www3.nd.edu/~lemmon/courses/ee224/web-manual/web-manual/lab7/node5.html | What is an Interrupt Handler? | What is an Interrupt Handler? Let's consider a program that the MicroStamp11 is executing. A program is a list of instructions that the micro-controller executes in a sequential manner. A hardware event is something special that happens in the micro-controller's hardware. An example of such an event is the RESET that occurs when pin 9 on the ...                                                 |
| ...                 | ...  | ...                                                                             | ...                           | ...                                                                                                                                                                                                                                                                                                                                                                                                         |
