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

    python3 ddg-retriever.py -i <path_to_input_file> -o <path_to_output_dir> -e <True/False>

Call without parameters to get information about possible parameters:

	python3 ddg-retriever.py
    
	usage: ddg-retriever.py [-h] -i INPUT_FILE -o OUTPUT_DIR [-e EXACT_MATCHES]
	                        [-d DELIMITER]
	ddg-retriever.py: error: the following arguments are required: -i/--input-file, -o/--output-dir



# Configuration

As input, the tool expects a CSV file with one column named `query`.
An exemplary input file can be found [here](input/queries.csv):

| query |
|-------|
| interrupt handler |
| sql injection|
| ...   |

To retrieve the search results as exact matches for the configured queries, you just need to run the following command:

    python3 ddg-retriever.py -i input/queries.csv -o output/ -e True

The tool logs the retrieval process:

	2019-08-27 15:52:16,369 ddg-retriever_logger INFO: Reading search queries from input/queries.csv...
	2019-08-27 15:52:16,370 ddg-retriever_logger INFO: 2 search queries have been imported.
	2019-08-27 15:52:18,875 ddg-retriever_logger INFO: Successfully retrieved search results for query: "interrupt handler"
	2019-08-27 15:52:18,880 ddg-retriever_logger INFO: Successfully parsed result list for query: "interrupt handler"
	2019-08-27 15:52:20,965 ddg-retriever_logger INFO: Successfully retrieved search results for query: "sql injection"
	2019-08-27 15:52:20,973 ddg-retriever_logger INFO: Successfully parsed result list for query: "sql injection"
	2019-08-27 15:52:20,973 ddg-retriever_logger INFO: Exporting search results to output/queries.csv...
	2019-08-27 15:52:20,974 ddg-retriever_logger INFO: 72 search results have been exported.

And writes the [retrieved data](output/queries.csv) to the configured output directory:

| query               | rank | url                                                                             | title                         | snippet                                                                                                                                                                                                                                                                                                                                                                                                     |
|---------------------|------|---------------------------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| "interrupt handler" |   1  | https://www3.nd.edu/~lemmon/courses/ee224/web-manual/web-manual/lab7/node5.html | What is an Interrupt Handler? | What is an Interrupt Handler? Let's consider a program that the MicroStamp11 is executing. A program is a list of instructions that the micro-controller executes in a sequential manner. A hardware event is something special that happens in the micro-controller's hardware. An example of such an event is the RESET that occurs when pin 9 on the ...                                                 |
| "interrupt handler" |   2  | https://en.wikipedia.org/wiki/Interrupt_handler                                 | Interrupt handler - Wikipedia | In computer systems programming, an interrupt handler, also known as an interrupt service routine or ISR, is a special block of code associated with a specific interrupt condition. Interrupt handlers are initiated by hardware interrupts, software interrupt instructions, or software exceptions, and are used for implementing device drivers or transitions between protected modes of operation ... |
| ...                 | ...  | ...                                                                             | ...                           | ...                                                                                                                                                                                                                                                                                                                                                                                                         |
