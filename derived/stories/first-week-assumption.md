---
slug: "first-week-assumption"
title: "What an analyst assumes in the first week"
serves: ["id-guid-identifier", "first-assumption-correct"]
page: "columns"
---

# What an analyst assumes in the first week

Of all the naming misses in Groups360's databases, this family may have caused more grief than any other. It comes from the way data analysts read the data.

Within a few days of looking at the data models, an analyst learns what the common words mean. A column called `id` is a bigint primary key. A column ending in `_id` is a foreign key to the table it is named for. A column called `guid` is a uuid, and one ending in `_guid` points to another table's `guid`, often in another database. The words declare both the type and the job of the column, and the pattern is so common that the assumption forms almost at once.

After that, the analyst stops checking and starts guessing from the name. When the name is honest, the guess is right and the work moves fast. When one column breaks the pattern, such as a vendor's reference stored in `external_id`, the guess is wrong in a way nothing warns about. The name promises a foreign key to a table called `externals`, and no such table exists. The full word `identifier` avoids the false promise, because it makes no claim about type or function.

The damage also spreads. One `_id` column that does not behave like the others means every `_id` column has to be checked, and the convention stops saving anyone time. One real table where this happened is told in `shape-sorter`.
