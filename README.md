# TradingContest

## API
Every request is a JSON object where one of the properties is `command` and its value is the type of request. Currently the following request types are supported:

- `book`
    - No arguments
    - Returns an object with `buy` and `sell` properties. Each of them contains an array of corresponding orders. Each order is an object with `symbol`, `sign`, `price`, `volume` and `time` properties (see `lib.py`).
- `account`
    - `account`
    - Returns an object where each property is one of the symbols and the value is how much of it is stored in the given account. The value can be negative.
- `buy`
    - `account`
    - `symbol`
    - `price`
    - `volume`
    - Returns an object with `id` property which is the id of the created order if it was placed to the book, or `None` if it was already executed.
- `sell`
    - Symmetrical to `buy`
- `cancel`
    - `id`
    - Cancels order with the given id. Returns an empty object.
- `register`
    - `account`
    - Creates new account with the given name. Returns an empty object.
- `history`
    - No arguments
    - Returns an array of `(time, price, volume)` tuples.

And if there is an exception during the request handling, an object with `error` property is returned. The value of this property is the error text.