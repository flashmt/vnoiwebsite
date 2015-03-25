# Ensure we are in the right directory
# cd "$(dirname "$0")"

total_error_code=0

for f in spec/*.rb; do
  echo "Executing test: $f"
  if [ -z "$TRAVIS_TEST_ENV" ]; then
    echo "Testing on local"
    bundle exec rspec $f --format documentation --format html --out "output/$f.html"
    total_error_code=$(($total_error_code + $?))
  else
    echo "Testing on travis"
    bundle exec rspec $f
    total_error_code=$(($total_error_code + $?))
  fi
done

if [ -z "$TRAVIS_TEST_ENV" ]; then
  echo "Creating report"
  rm -f report.html
  cat output/spec/*.html > report.html
fi
echo "Error: $total_error_code"
exit $total_error_code
