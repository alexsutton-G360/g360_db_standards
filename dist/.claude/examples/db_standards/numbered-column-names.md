# Check what a numbered column name is really saying

Rule line `RDBNM8` in `db_naming_conventions.md`. Temperature: Judgment call. Origin: house.

## Full rule

Digits in a column name are fine when the numbers are the point. Names that differ only by number, like `contact_1` and `contact_2`, tell a reader the two are parallel slots. A pair like `contact` and `contact_2` tells the reader that one outranks the other. If that is not what the data means, the reader's first assumption is wrong.

Before adding a numbered column, ask what the second column really is. If it is the newer version of the first, or one is the main one, name each for what it is.

Good: `contact_1` and `contact_2`, when there are two parallel contacts
Good: `primary_contact` and `secondary_contact`, when one outranks the other
Bad:  `contact` and `contact_2`
