# Coin Mixer 🐍💎

As Bitcoin is not an anonymous protocol (but a pseudonymous system), our **Coin Mixer** PoC is an approach to maintaining privacy on our Aquario Coin Network (for a tiny small fee 😉)!

We use [Coin Mixer Server API endpoints]() to deploy our sophisticated mixer algorithm to your coin deposit!


<p align="center">
<img src="./imgs/Jobcoin_Mixer.png" width="90%" align="center" style="padding:1px;border:thin solid black;" />
</p>


#### To install our Jobcoin Mixer CLI, follow the instructions below.

----


## Set up your `.env` file

To follow best practices, we set our variables and secrets into a `.env` file, which can be copied from `.env_sample`:

```
cp .env_sample .env
```

Set the following variables:

```
API_ADDRESS_URL = ''
API_TRANSACTIONS_URL = ''
SIGNIFICANT_DIGITS = 17
HOUSE_ADDRESS = 'Jobcoin-House'
FEE_PERCENTAGE = 0.1
WITHDRAW_MAX_VALUE = 1
```

#### What is `HOUSE_ADDRESS`?

The ephemeral `hex` *deposit address* moves the coins to this address, where it's then mixed with other coins.


#### What is `SIGNIFICANT_DIGITS`?

As Jobcoin Mixer deals with float transactions, this variable sets the desired precision when converting strings to float.

#### What is `FEE_PERCENTAGE`?

An integer number representing the percentage fee to be collected for the mixing service. Set to 0 for no fee.


#### What is `MAX_WITHDRAW_VALUE`?

Set the value for small withdrawal values for which Jobcoin Mixer will move from the House address to each personal addresses.

Jobcoin Mixer *cares about your privacy*, so setting this to smaller values makes the transactions more discrete!

If you would like to have Jobcoin Mixer withdrawing all coins in one unique transaction, simply leave this constant empty (`None`).


----
## Install Jobcoin

You can install Jobcoin either via `setup.py` or by running it straight from the executable (`jobcoin/cli.py`).

## With `setuptools`

Install `jobcoin 0.0.1` with:

```
make install
```

Now you can run:

```
jobcoin
```

## With `cli.py`


### Install dependencies in a virtual environment

You can use either `virtualenv` or `pipenv`.

#### Using virtualenv

Install `virtualenv`:

```
pip install virtualenv
```

Creating and sourcing the environment:

```
virtualenv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

You can always check what is installed in your environment with:

```
pip freeze
```

#### Using pipenv

Install `pipenv`:

```
pip install pipenv
```

Create a new virtual environment using pipenv:

```
pipenv install
```

Activate:

```
pipenv shell
```

You can always check what is installed in your environment with:

```
pipenv graph
```

Remove the prefix `jobcoin.` from every import at the top of the source files `api.py`, `cli.py`, and `jobcoin.py`.

Then run:

```
./jobcoin/cli.py
```

---

### Example of usage


#### Successful flow


<p align="center">
<img src="./imgs/Mixer_example.png" width="90%" align="center" style="padding:1px;border:thin solid black;" />
</p>

#### Personal address is not unused

<p align="center">
<img src="./imgs/Mixer_example_error.png" width="90%" align="center" style="padding:1px;border:thin solid black;" />
</p>

#### Insufficient funds

<p align="center">
<img src="./imgs/Mixer_example_error_2.png" width="90%" align="center" style="padding:1px;border:thin solid black;" />
</p>

#### Given coin amount is zero

<p align="center">
<img src="./imgs/Mixer_example_error_3.png" width="90%" align="center" style="padding:1px;border:thin solid black;" />
</p>

----

## Developer corner

If you are developing Jobcoin Mixer, you have the following resources:

#### Running a linter

```
make lint
```

#### Running unit tests

```
make test
```

#### Cleaning dist, dev, test, files

```
make clean
```

Note: to be able to run tests and linter, install:

```
pip install -r requirements_test.txt
```

---

## Next Steps

* Improve unit tests. Add missing tests for `test_jobcoin.py`, `test_cli.py`, and `test_util.py`. Add tests for failures and success, with better mocking and fixtures.
* Improve private method `_is_empty()` as it loops over all the transactions address. As the list increases, this will take too long. Maybe we should simply check whether the address has zero coins? Should we think about a cache solution?
* Deal with the increased size of the list of transactions being pulled from the server every time. Should we think about a cache solution?
* Convert the code to pure Python 3 (e.g., `-> return` in the module name, etc.). Make sure the dependencies install Python3 libraries. Make sure the code run in Python3.
* Adding `logging` everywhere, with different types of logging levels.
* Improve rules for linting.

