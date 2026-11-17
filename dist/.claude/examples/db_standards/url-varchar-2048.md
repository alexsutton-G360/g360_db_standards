# Store a URL in varchar(2048)

Rule line `RDBCL12` in `db_column_conventions.md`. Temperature: Default. Origin: general.

## Full rule

Use `varchar(2048)` for a column that holds a URL. It is a good default limit, and about as big as a URL should be. Go longer only if it really makes sense to, which it probably does not. If the URL comes from something you know and control, you are encouraged to use a smaller field. You do not have to, but a smaller limit is better design whenever the data allows it (*rule: smallest-honest-varchar-limit*).

Because: no standard limits the length of a URL, but around 2,000 characters works in virtually any combination of browser, server, and search tooling, and the sitemap protocol caps URLs at 2,048. A URL that follows the standard is plain ASCII, so 2,048 characters is 2,048 bytes in the warehouse, far under its ceiling.

Good: `varchar(2048)` for an image URL
Bad:  `text`, or `varchar(65535)` for a URL
