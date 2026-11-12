---
slug: "image-documents"
title: "When the document is the data"
serves: ["unbounded-data"]
page: "columns"
---

# When the document is the data

A design at Groups360 for an image-processing service split the work into discrete steps. The older approach was a single process: query an image vendor, get back a document describing the images for a property, parse it, and write the results to the database. The new design split that into stages. One step queries the vendor and stores the document it gets back. A second step reads the stored document and cuts it into an image set. A third pushes the image set out to the services that need it. Each stage can be run, tested, and repeated on its own.

That design had one consequence for the database. The stored documents would be large. Each is only a collection of URLs, but one hotel's document from the vendor can run past 100,000 characters. The operational Postgres databases can hold that as a `text` column or a very wide `varchar` without trouble, but no choice of type makes it fit in the data warehouse.

The length of such a document is not a decision anyone makes. It is simply how long the vendor's response is, so the length is a fact about the data. A limit would mean inventing a rule the data does not have, which is the opposite of what a constraint is for. What matters is where the data goes next. Raw documents like this are rarely useful in the warehouse, and the likeliest outcome of the conversation with the data teams is a note that the table is never to be synced, so a sync does not break. If the warehouse does need the data, the options are to keep only the first 65,535 characters (see `multibyte-text` for why that count needs care) or to move the documents to object storage and keep a reference in the table.

The project was later pared down, and the large documents never became a live problem. The questions it raised are still the ones to ask of any column that could grow that large.
