# kaggle-avito

Code for kaggle competition: Avito Duplicate Ads Detection

Given 2 items and information of their location, images category, ad title, ad description, price and metro, kagglers are asked to tell whether they are duplicate ads of the same product

Codes are written in 2-3 days, achieving 127/548(top 25%) on private leaderboard.

Model conducted: random forest classification from sklearn

Missing pairs is always a problem in both classification and regression. i.e., among given item pairs, price or title or images of some of them are missing. To solve this problem, feature importance should be measured, e.g., missing pairs of which feature are important. And then separate models are trained for items with or without these features. In experiments, info about price or image are found to have a large impact on the result.

Features are price diff(abs and relative), latitude diff(abs), longitude diff(abs), title similarity(Jaccard Similarity), description similarity(same as title similarity), distance between images(see below for details)

Images are hashed in such a way(called dhash, credit to Kaggler Run2): the difference between i and i+1 element in the image matrix is computed line by line, and 1 is used for positive diff and 0 for negative. Then the difference is encoded in hexadecimal format for storage reduction. Hamming distance is used.

Other informations such as location and metro are dumped since adding them do no improvement on the result of validation set.
