#!/usr/bin/env python3
import csv
import sys
import os

def read_lookup_table(lookup_file_path):

    lookup_dict = {}

    try:
        with open(lookup_file_path, mode='r', newline='', encoding='ascii') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dstport = row['dstport'].strip()
                protocol = row['protocol'].strip().lower()
                tag = row['tag'].strip()
                key = (dstport, protocol)
                lookup_dict[key] = tag

    except Exception as e:
        print(f"Error reading lookup file: {e}")
        sys.exit(1)
    return lookup_dict

def parse_flow_log(flowlog_file_path, lookup_dict):

    tag_counts = {}
    port_protocol_counts = {}
    
    try:
        with open(flowlog_file_path, mode='r', encoding='ascii') as logfile:
            for line in logfile:
                fields = line.strip().split()

                if len(fields) < 14:
                    print(f"Incorrect log line: {line}")
                    continue
                
                dstport = fields[6].strip() #6th field is destination port
                protocol_num = fields[7].strip() #7th field is protocol number
                
                if dstport == '-' or protocol_num == '-':
                    print(f"Skipping log entry with missing fields: {line}")
                    continue

                protocol = map_protocol_number(protocol_num).lower()
                
                key = (dstport, protocol)
                
                tag = lookup_dict.get(key, 'Untagged')
                
                tag_counts[tag] = tag_counts.get(tag, 0) + 1 # Updating tag counts
                
                port_protocol_key = (dstport, protocol)
                port_protocol_counts[port_protocol_key] = port_protocol_counts.get(port_protocol_key, 0) + 1 # Updating port and protocol counts

                
    except Exception as e:
        print(f"Error reading flow log file: {e}")
        sys.exit(1)
        
    return tag_counts, port_protocol_counts

def map_protocol_number(protocol_num):

    protocol_map = {
        '1': 'icmp',
        '6': 'tcp',
        '17': 'udp',
        '2': 'igmp',
        '89': 'ospf',
        '132': 'sctp',
        '47': 'gre',
        '50': 'esp',
        '51': 'ah'
    }
    return protocol_map.get(protocol_num, 'unknown')

def write_output(output_file_path, tag_counts, port_protocol_counts):

    try:
        with open(output_file_path, mode='w', newline='', encoding='ascii') as outfile:
            writer = csv.writer(outfile)
            
            # Write tag counts to output file
            writer.writerow(['Tag Counts:'])
            writer.writerow(['Tag', 'Count'])
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[0]):
                writer.writerow([tag, count])
            writer.writerow([])
            
            # Write port/protocol counts to output file
            writer.writerow(['Port/Protocol Combination Counts:'])
            writer.writerow(['Port', 'Protocol', 'Count'])
            for (port, protocol), count in sorted(port_protocol_counts.items(), key=lambda x: (int(x[0][0]), x[0][1])):
                writer.writerow([port, protocol, count])
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

def main():

    if len(sys.argv) != 4:
        print("Insuffecient parameters passed")
        sys.exit(1)
        
    flow_log_file = sys.argv[1]
    lookup_table_file = sys.argv[2]
    output_file = sys.argv[3]
    
    # Validate output directory
    if not os.path.isfile(flow_log_file):
        print(f"Flow log file does not exist: {flow_log_file}")
        sys.exit(1)
    if not os.path.isfile(lookup_table_file):
        print(f"Lookup table file does not exist: {lookup_table_file}")
        sys.exit(1)
    
    # Read lookup table
    lookup_dict = read_lookup_table(lookup_table_file)
    
    # Parse flow log
    tag_counts, port_protocol_counts = parse_flow_log(flow_log_file, lookup_dict)
    
    write_output(output_file, tag_counts, port_protocol_counts)
    
    print("Processing complete.")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main()
