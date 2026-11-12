---
slug: "derived-by-process"
title: "The value that never needed a process"
serves: ["calculated-columns"]
page: "columns"
---

# The value that never needed a process

In 2018, Groups360 stored a property's latitude and longitude as two plain columns, kept current by a script. A separate application process took those two values and built a point value from them whenever it ran. The point depended on nothing but the two columns beside it. It was a function of them and nothing more.

For years that caused no trouble. The process worked, and nothing about the design looked like a mistake. Then, three or four years in, it began to matter. An application process is code, and code fails. Sometimes an earlier step stopped before the point was written. Sometimes the process was never started when it should have been. Each time, the point was left behind with no error and no trace, while the two columns it came from moved on without it.

By the time the gaps were a problem, they were a problem everywhere. The fix took until 2025, many developers, and about six months from planning to finished work, because the stale values, and the code that produced them, had spread through the database. The finished fix is short to describe: the point became a generated column over latitude and longitude.

A generated column cannot disagree with its inputs. The database computes it whenever they change, and nothing can write to it directly. The failure was never about careless code. A derived value that code keeps in step is only as reliable as every run of that code, and a generated column has no run to miss. That is the case for the rule, and the reason it is a default and not a preference. The point never needed a process at all.
