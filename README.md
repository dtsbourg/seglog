# seglog.py

Splits a log file into multiple files based on a parameter predicate

### Arguments

  * `-h` : help message for this script
  * `-i` : relative path to input file
  * `-o` : prefix for output file name
  * `-p` : string representation of predicate 

### Default settings

  * `output_path` is the current directory
  * headers are displayed on each split file
  * segmented files are prefixed with `flight-{n}.txt`

### Available operators
  
  * `>` 
  * `>=`
  * `<`
  * `<=`
  * `==`
  * `!=`

### Example usage

    >>> python seglog.py -i log.txt -o flight -p "state >= 0 && acc_x > 20"
    >>> python seglog.py -i ../Desktop/Log_file_201.txt -p "gps_status==2 || healthy != 0"
