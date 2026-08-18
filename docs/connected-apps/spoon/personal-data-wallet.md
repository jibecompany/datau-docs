# Personal Data Wallet

## Overview

The **Personal Data Wallet** (v0.0.9) at [wallet.datau.jibe.cloud](https://wallet.datau.jibe.cloud)
is the citizen-facing data-control layer of the DataU platform. It empowers you to take ownership of
your personal data by storing it in a structured, categorised wallet that you fully control.

The wallet implements GDPR-rooted controls — **access, rectification, erasure, and portability** —
giving you genuine data sovereignty rather than passive participation. Rather than having data
collected in the background, you actively choose which data items to add, categorise each item, and
give **explicit consent** each time an item is saved and made available for sharing with a research
organisation or application.

The wallet covers a comprehensive range of food-related and sociodemographic data types — from basic
identity (name, age, address) to detailed food-behaviour attributes (planning persona, shopping
habits, food-label attitudes, dietary preferences, sustainability factors).

You can connect the wallet to the SPOON Dashboard and other apps, and at any point review what data
you have shared and with whom via [DashboardU](../../data-subjects/dashboardu.md).

## Getting started

1. Navigate to [https://wallet.datau.jibe.cloud](https://wallet.datau.jibe.cloud), or open it from
   the SPOON Dashboard.
2. Log in with your DataU account.
3. The home screen shows **Welcome, [Name]!** and a list of your current data items.
4. If no items exist yet, click **+ Create a new Data Item** to add your first one.

## Creating a data item

Click **+ Create a new Data Item** to open the creation form with three fields:

- **Title** — select the type of data from a dropdown list (see [Available data types](#available-data-types)).
- **Category** — classify the data: `IDENTITY`, `CONTACT`, `FINANCIAL`, `HEALTH`, or `MISC`.
- **Value** — enter the actual data value in the text area.

!!! warning "Consent is mandatory"
    Click **Save** and you will be redirected to DataU to give consent for sharing this data item.
    This consent step is **mandatory** and ensures you explicitly authorise any use of your data.
    Click **Back** to cancel without saving.

## Available data types

=== "Identity & Contact"

    - Name, First Name, Last Name, Email, Phone Number
    - Address, Country, Region, Nationality, Language, Religion
    - Age, Age Range, Gender, Education, Occupation, Income
    - Household Size, Household Type

=== "Health & Physical"

    - Health Status, Height, Weight, Diet-related diseases, Mobility
    - Vegan, Vegetarian, Flexitarian, Pescatarian, Omnivore
    - Animal-based foods, Plant-based foods, Fresh fruits, Fresh vegetables
    - Gluten-free foods, Milk and dairy products, Organic products

=== "Food behaviour & shopping"

    - Planning Persona, Meal Planning Horizon, Pre-Trip Meal Planning
    - Shopping List Frequency / Adherence, Trip Planning Extent Score
    - Top Buying Influences Ranked, Primary Priority Selection, Primary Purchase Location
    - Unplanned Item Count, Bulk Buying Frequency Score, Promotions Influence Level
    - Place of purchase, Main Store Type Category, Store Accessibility Easy Score
    - Food Label Attitude (Trust, Understanding, Environmental/Social/Price Info, Visual Format, …)
    - Food Label Recognition, Food Options Satisfaction, Food Offering Health
    - Dietary Alignment Score, Planning Confidence Score, Planning Barrier, Planning Tool
    - Waste Consideration Frequency, Disposal frequency / quantity / reasons
    - Eco-score, Carbon footprint, Packaging type, Sustainability factors
    - Transportation, Access Method, Access Improvement Factors, Hard-To-Find Products
    - Photo Upload

## Sidebar

- **Connected Apps** — quick link back to the SPOON Dashboard
- **Documents → Terms & Conditions** — platform T&Cs PDF
- Your user profile: name, email, initials avatar, and **⋯** menu for account options
