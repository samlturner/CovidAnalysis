curl -s https://coronavirus.health.ny.gov/covid-19-travel-advisory | grep -A 100 "toc_886" | sed -n '/ul/,/ul/p' | head -n -1 | sed 's/<ul>//g' | sed -e 's/<li>\(.*\)<\/li>/\1/' | sed 's/^[[:space:]]*//g'