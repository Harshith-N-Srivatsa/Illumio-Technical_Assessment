# Illumio-Technical_Assessment
This repository contains the solution to the Technical Assessment for Illumio

Name: Harshith Narasimhan Srivatsa

email ID: hns.harshith@gmail.com

Ph No.: +1 623 287 5532


The solution for the technical assessment will parse flow logs and map the destination port and protocol combinations to the respective tags based on a lookup table. The solution takes two input files: a flow log text file and a lookup table csv file, and produces an output text file that provides counts of matched tags and port/protocol combinations.

## Assumptions
1. Log Format: Based on the reference given in the technical assessment, the solution follows AWS VPC flow log format (version 2). It will not work with custom formats or older versions.
2. Input Data: The flow log files must be in plain text with space separated values. Line delimeter is a new line character. Each line must follow the expected structure of version 2 flow logs. 
3. Case Sensitivity: The protocol names in the lookup table are case insensitive.
4. Field Validity: The solution assumes that the destination port and protocol fields in the flow logs are valid integers and within the appropriate range.
5. Lookup Table Size: The solution expects the lookup table to follow format provided in the assessment. It can handle up to 10,000 mappings.
6. Protocol Map: The solution provides the mapping of protocol numbers to corresponding names for 9 most frequently occuring protocols. Rest will be tagged as unknown. This can be extended if required.
7. Output File: There will be 1 output file. Output file will follow the sample output format mentioned in the assessment details.
8. Environment: The solution assumes that Python 3 is installed for it to execute. It does not depend on non-default libraries or packages like Hadoop, Spark, or Pandas.

## Running the Script
To execute the code, use the following command:

python flow_log_parser.py <flow_log_file> <lookup_table_file> <output_file>

Example: python flow_log_parser.py sample_logs.txt lookup_table.csv output.txt

## Test cases
1. Normal flow log and lookup table

Description: A normal case with a flow log and a lookup table that matches ports and protocols to tags.
Outcome: The program correctly mapped the ports and protocols from the flow log to their respective tags and generated accurate counts. The output was as expected.

2. Missing field in flow log (-)

Description: A flow log containing missing fields represented by - for destination port and protocol number. Also tested for cases where there are less than 14 fields indicating a missing field.
Outcome: The program identified and skipped log entries with missing fields. These entries were excluded from the final count and the output file generated only contained valid entries. 

3. Flow log with unknown protocol

Description: A flow log with an unknown protocol number, which is not listed in the protocol map.
Outcome: The program handled the unknown protocol correctly by categorizing it as unknown. All other entries with known protocol numbers were processed as expected, and the tag counts were correct.

4. Multiple ports/protocols mapped to the same tag

Description: The lookup table contained multiple entries mapping different ports and protocols to the same tag.
Outcome: The program successfully handled multiple mappings to the same tag and correctly combined the counts for the tag. The port/protocol combinations were also counted correctly.

5.  Empty flow log file

Description: An empty flow log file with no entries.
Outcome: The program handled the empty file producing an output file with no tag counts or port/protocol counts, as expected. No errors were encountered during execution.

6. Lookup table with non-matching ports/protocols

Description: A flow log containing entries for ports and protocols that are not present in the lookup table.
Outcome: The program correctly categorized these entries as Untagged since no matching port/protocol pairs were found in the lookup table. The counts for untagged entries and the port/protocol combinations were accurate in the output.

7. Incorrect file names or file types 

Description: Incorrect file names or file types or paths were fed to execute the program.
Outcome: The program throws an exception in such cases indicating the file/path that is incorrect.

8. Case Insensitivity in Protocol Mapping

Description: A lookup table containing a mix of uppercase and lowercase protocol names and a flow log with standard numeric protocol numbers.
Outcome: The program correctly matched protocols regardless of case, assigning the correct tags and producing accurate counts for tag mappings and port/protocol combinations.
