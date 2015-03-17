# VNOI functional tests

## Setup:

- Run commands:

```bash
git clone https://github.com/VNOI-Admin/vnoiweb_test.git
cd vnoiweb_test
./setup_linux.sh # ./setup_mac.sh for MacOS
```

- Setup Firefox, version below 36

## Project structure:

- spec: the tests!
- content: what string should a page have (e.g. Forum page should have strings: "Các kỳ thi trực tuyến", "Online Judge", etc.)
- helper.rb: basic setup & helpful methods
- Gemfile: project dependencies

## Run the test:
- Run command:

```bash
./runall.sh
```

- Look at `report.html` for HTML reports

## Troubleshoot:

### Could not find gem
- Error:
```
Could not find gem 'capybara-screenshot (~> 0.3.21) ruby' in the gems available on this machine.
```

- Reason: New gem was added as dependencies --> you need to install those
- How to fix:

```bash
bundle install
```
