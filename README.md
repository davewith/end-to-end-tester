# End To End Tester example

## Setup process

So how do you go about implementing this testing into an existing project? I'm
going to use ModelW as my base, and will do a simple log in screen which we want
to test on iPhone Chrome and Windows Chrome using browserstack.

### 1: Clone the browserstack template project into your project root

_Eventually this will become part of ModelW with nice custom shared
functionality and shared step definitions_

`git clone https://github.com/browserstack/cucumber-js-browserstack.git tester`

### 2: Install dependencies

`cd tester && npm install`

### 3: Set your browserstack credentials

_Found in your dashboard under "Access key"_

`npx setup --username userName --key accessKey`

### 4: Run sample local test

`npm run sample-local-test`

### 5: Customise for our use

Add a script to test on our local machine
`"test": "cucumber-js features/single.feature",`

Make sure we have installed our browser driver. eg. For
[Chrome](https://chromedriver.chromium.org/downloads) (_Note: You must match
versions_) _@TODO: Instructions for exporting path, where to install etc. For
now just include an absolute path_

Run chromedriver
`/usr/local/share/chromium-browser/chromedriver --url-base=/wd/hub --port=4444`

## Test writing process

Create a feature file in features, and write the acceptance test using Gherkin.
_Organise it however you feel suits your project, eg. folder per epic, file per
epic or file per US._

I'll keep it simple and do a feature for the US.

```
Feature: Login functionality

  Scenario: Login with different types of credentials
    Given I am on the login page
    When I enter "<email>" and "<password>"
    Then I should see "<message>"

    Examples:
      | email   | password  | result    |
      |         |           | Empty     |
      | emailN  | passwordN | Incorrect |
      | emailY  | passwordY | Welcome   |
```

And the 3 step definitions required:

```js
Given(/^I'm on the (.+) page$/, async function (page) {
    await this.driver.get(`http://localhost:3000/${page}`);
});

When(
    "I attempt to log in using {string} and {string}",
    async function (email, password) {
        await this.driver.findElement(By.id("email")).sendKeys(email);
        await this.driver.findElement(By.id("password")).sendKeys(password);
        await this.driver.findElement(By.css('button[type="submit"]')).click();
    }
);

Then("I should see a message with {string}", async function (expectedText) {
    const actualDiv = await this.driver.wait(
        until.elementLocated(By.id("user-message")),
        5000
    );
    const actualText = await actualDiv.getText();

    assert.ok(
        actualText.toLowerCase().includes(expectedText.toLowerCase()),
        `Expected ${expectedText} in message`
    );
});
```

I hope this example shows how with just a few step definitions, we can quickly
create and maintain a huge number of test variations.

Also, I hope that it's clear to see how these semi-cryptic selenium actions can
easily be abstracted out into a shared With-Test-Library, because at the end of
the day, we don't really do much on a website other than click and type.

So now we run our tests, to make sure they both run and fail.

```
✖ Then I should see a message with "Empty" # features/step_definitions/then_steps.js:7
    AssertionError [ERR_ASSERTION]: Expected Empty in message
```

Perfect. Now lets code the solution.

_Tip: Sometimes it's good to confirm the tests are good, by typing the target
words into a Vue page, to make sure the tests will pass_

So, now I'll add the simple login page, using a message component and using the
standard login ModelW provides, and once the tests pass, the code is working. If
someone says otherwise, then at that point, the tests need to change, not the
code!

### Someone finds a bug

OK, there's a bug... So my method only checks if I get an OK from the API, it
doesn't check if the user is authenticated or not. But all tests pass...What to
do???

### 1: Make the test fail! The tests are insufficient. Lets target the bug.

    | good@test.com   | passwordY | Successful |
    | bad@test.com    | passwordY | Failed     |

### 2: Fix the issue:

In this case it is of course that we didn't implement any authentication in
Django, nor were checking for it Nuxt.

### 3: Tests pass:

So we run it locally with `npm run test` and all good, so we do it

on Browserstack with the devices/systems we want `npm run bs-test`, and again
all good, and with nice
[recordings](https://automate.browserstack.com/dashboard/v2/public-build/ZjJMTTZDcVZnc2Ntdjd1ekg3ditxeHJ0M0kvemVNc09wVnp0RGxXWGgwOTEwbXR3K1FPVFpVaDU0b2xXMkR0cE5rU0RpTzEyREwzUDRZU2IrWU1wOUE9PS0tQmwxb0QrZVRiR2s5YjhFNUxRQ0FlUT09--cf6d314a1f6ebfc3b7392254e85250d4c272fae3)
to send to the PMs.

![Browserstack run](/readme_images/bs001.png)

![Browserstack video](/readme_images/bs002.png)

### Note about test data:

Testing when data changes is always a time sink, and at best we have scripts
that create and delete when we need. But is there a better way? Well yes, using
fixtures. The easiest way is to create "worlds" either manually if small or with
helper scripts, and then dump out what you need (_the usual caveats apply
regarding contenttypes and auth.permissions etc_):  
`pmanage dumpdata people.User --indent 4 --output users.json`

Now we can load any fixture in any test we want and suddenly we have different
worlds at our fingertips.

## Final tips:

Prioritise low coupling over DRY. Tests are a different animal to source code
and need to be treated differently. Don't be afraid of repeating yourself
because tests have a habit of drifting apart from one another. (eg. "What about
adding a pause after clicking only that menu button", "on this page what about
reversing the order..."). Therefore, modularise as much as you can, but don't go
over board trying to create a huge test that covers all. Be specific.

Do whatever feels useful to you! You know your project and the bugs that
have/will creep in, so implement these tips whatever way you please, and we'll
all naturally find our equilibrium. BDD is a mindset more than a stack, so as
long as you remember to think from the business point of view, you can't go far
wrong!

As a dev, resist the urge to fill the feature files with procedural programming!
Keep the feature file completely free from implementation details. If tomorrow,
we can all use websites telepathically, your feature files should still work!
The step definitions are where your code brain belongs.
