#!/bin/bash
#  This script installs Python dependencies. If no arguments are supplied,
#  only mandatory dependencies are installed. if `-d|--dev|--development`
#  switch is supplied, optional dependencies are installed also.


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REQUIREMENTS_FILE="$DIR/requirements.txt"


# Default values before parsing command line args
DEVELOPMENT=false


# Get command line arguments...
while [[ $# -gt 0 ]]; do
	key="$1"
	case $key in
		-d|--dev|--development)
		DEVELOPMENT=true
		;;
		*)
		# unknown option, skip
		;;
	esac
	shift
done


#  Echo to standard err
log() {
	echo "$@" 1>&2
}



# Gets line number based on optional reqs regex. If not there, exit
get_line_number () {
	if ! local line_number=$(grep -rPn '[O|o]ptional' "$REQUIREMENTS_FILE" | cut -d ':' -f 1); then
		log "Requirements file does not have optional line"
		exit 1
	fi
	echo "$line_number"
}


install_pip_reqs() {
	if [[ $DEVELOPMENT = 'true' ]]; then
		log "Installing ALL dependencies"
		pip install -r "$REQUIREMENTS_FILE"
	else
		log "Installing only required dependencies"
		pip install -r <(head -n $(get_line_number) "$REQUIREMENTS_FILE")
	fi
}


install_npm() {
    rm -rf "$DIR/node_modules"
    cd "$DIR" && npm install
}


main() {
    install_pip_reqs
    install_npm
}


main
