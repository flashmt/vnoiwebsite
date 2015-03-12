# # Unit Testing Guide

## Why we need testing

- Testing while developing makes sure that the changes you make doesn't have unexpected effects on existing codes and functionalities.
- Unit Test covers a small area of code such as a single function. Typically, each unit test sends an input to a method and verify that the method returns the expected value.

## What we test
For vnoi_website django project, we need to test our custom methods in:

1. Models
2. Forms
3. Views


## How we test

1. Write tests covering areas (including models, views, forms) - which maybe affected by your new codes (can write test before implementing or right after the first draft of implementation). Write tests as many as possible.
2. Run test suites (read django document see how). For example, to run all test cases in app forum:

    ```bash
    python manage.py test forum
    ```

3. Fix bugs or change code
4. Repeat step 2, 3 until all testcases are passed

## Notes for vnoi_website project

1. We use [django fixtures](http://django-testing-docs.readthedocs.org/en/latest/fixtures.html) to initialize database for testing. Everyone shares the same fixtures which can be found in **main/fixtures**. If you create your custom fixtures, put into the folder.
2. Testing structure

	![Testing Structure](https://github.com/VNOI-Admin/vnoiwebsite/tree/master/documents/testing/test_structure.png)

3. Run tests whenever code is pullled or pushed 

## Useful links
1. See example source code in **forum/tests/**
2. vnoi_website Django Fixture [link](https://github.com/VNOI-Admin/vnoiwebsite/blob/master/documents/database/django_fixtures_to_initialize_data.md)
3. [http://toastdriven.com/blog/2011/apr/10/guide-to-testing-in-django/](http://toastdriven.com/blog/2011/apr/10/guide-to-testing-in-django/)
4. [Test-driven Django Tutorial](http://www.tdd-django-tutorial.com/)



