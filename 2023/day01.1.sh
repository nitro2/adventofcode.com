sed 's/[^0-9]*//g' | sed 's/\(.\).*\(.\)/\1\2/' | awk '{s = ($1 > 9 ? $1 : ($1)*11) ; sum += s; print s} END {print sum}'
