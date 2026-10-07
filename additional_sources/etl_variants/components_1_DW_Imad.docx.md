# Text-only document extract

Source document: Assignment_1_DW_Imad.docx

Images and layout omitted. Claims below are source text, not independently verified results.

University of Management & Technology

Department of Artificial Intelligence

CS439 — Data Warehouse  |  project #01  |  Spring 2026

Name: Syed Muhammad Imad ID:Syed Muhammad Imad






Question 1 (CLO-1) — 10 Marks

Explain what OLTP and OLAP are using GlobalMart as an example. Highlight their main characteristics, purposes, and differences.





1. OLTP — Online Transaction Processing

OLTP systems handle the day-to-day operational transactions of a business. They are built for speed — processing thousands of small, fast database operations simultaneously without delay. Every time a real-world event occurs at GlobalMart, the OLTP system records it instantly.

What OLTP Does at GlobalMart

GlobalMart runs millions of OLTP transactions daily across its physical stores, online platform, and warehouse network. Here is what happens at the database level for each event:

A customer buys a product at a store: the system inserts a transaction record containing customer ID, product ID, quantity, price, and timestamp.

A supplier delivers Lays chips to a warehouse: the system inserts a shipment record with supplier ID, product ID, quantity received, arrival date, and warehouse location.

A customer returns a shampoo: the system updates inventory (+1 unit) and inserts a return record with customer ID, product ID, store ID, date, and refund amount.

A new soap is added to the product catalog: the system inserts a product record containing product name, category, price, and supplier ID.



Every one of these operations is triggered by a real-world event, processed in milliseconds, and executed by thousands of concurrent users — cashiers, customers, warehouse staff — all hitting the system at the same time. OLTP databases are highly normalized to eliminate redundancy and maintain data integrity across all these rapid operations.



2. OLAP — Online Analytical Processing

OLAP systems are built for analysis, not operations. They work on historical data to answer complex strategic questions that no OLTP system can handle efficiently. Where OLTP records what is happening right now, OLAP analyzes what has happened over time.

What OLAP Does at GlobalMart

GlobalMart's management, analysts, and regional executives use OLAP to drive decisions. These are the kinds of questions OLAP answers:

"What were the total sales of Lifeboy soap from March until now across the Punjab region, during the active promotion period?" — this spans months of data, filtered by region and promotion status.

"How much more or less crude oil did we receive from suppliers this year compared to last year?" — a year-over-year supply comparison across the entire supply chain.

"Which product category had the highest return rate in Q4 2025 across all regions?" — aggregating millions of return records across time, product, and geography simultaneously.



These queries scan months or years of data across multiple dimensions at once. OLAP databases are denormalized — data is pre-joined and flattened specifically for read speed. A fully normalized structure would require joining dozens of tables per query, which becomes catastrophically slow at terabyte scale. Denormalization trades storage space for query performance.



3. Why OLTP and OLAP Must Be Separate Systems

Running analytical queries directly on GlobalMart's OLTP database would be an operational disaster. A single heavy OLAP query scanning three years of sales data would require processing millions of records — while thousands of concurrent users are simultaneously inserting and updating data on the same system. The result: live transactions slow down or freeze entirely. Checkouts fail. Inventory updates stall. The entire operation grinds to a halt.

A separate Data Warehouse running OLAP workloads ensures that no analytical query ever touches the live operational system. The two serve fundamentally different purposes and cannot share the same infrastructure without one destroying the other.



4. OLTP vs. OLAP — Comparison Table

Feature

OLTP

OLAP

Full Form

Online Transaction Processing

Online Analytical Processing

Purpose

Run day-to-day operations

Support strategic decisions

Data Type

Current, real-time data

Historical data (months/years)

Operations

INSERT, UPDATE, DELETE

SELECT with aggregations

Query Type

Simple and fast

Complex and slow

Number of Users

Thousands (staff, customers)

Few (analysts, executives)

Database Design

Normalized (eliminates redundancy)

Denormalized (optimized for reads)

Response Time

Milliseconds

Seconds to minutes

Database Size

Gigabytes

Terabytes

GlobalMart Example

Recording a customer purchase or supplier delivery

Analyzing 3-year regional sales trends or supply comparisons







End of project
