import pandas as pd
import numpy as np
import random

videos = pd.read_csv("~/Downloads/USvideos.csv")


videos_sel = videos.drop(
        columns=["title", "tags", "channel_title", "thumbnail_link", "description"]
).assign(
        trending_date = lambda row: pd.to_datetime(row.trending_date, format='%y.%d.%m'),
        publish_time = lambda row: pd.to_datetime(row.publish_time).dt.tz_localize(None),
        days_to_trending = lambda row: (row.trending_date - row.publish_time).dt.days,
        trending_class = lambda row: np.where(
            row.days_to_trending <= 1,
            "fast",
            np.where(
                row.days_to_trending <= 3,
                "normal",
                "slow"
            )
        )
).drop(
        columns="trending_date"
)

#videos_sel.to_csv("../docs/youtube_videos_regression.csv", index=False)
def kaggle_split(videos_sel, is_regression):
    videos_sel = videos_sel.drop_duplicates(subset="video_id", keep="first")
    wanted = "days_to_trending" if is_regression else "trending_class"
    unwanted = "trending_class" if is_regression else "days_to_trending"

    random.seed(42)
    train_ids = random.sample(list(videos_sel.index), int(len(videos_sel) * .8))

    train = videos_sel.query("index in @train_ids").drop(columns=unwanted)
    test = videos_sel.query("index not in @train_ids").drop(columns=unwanted)
    display_test = test.drop(columns=wanted)
    solution = test.filter(items=["video_id", wanted])

    if is_regression:
        np.random.seed(42)
        random_days_to_trending = np.random.normal(
                test[wanted].mean(), 
                test[wanted].std(), 
                len(test)
        )
        sample = test.filter(
                items=["video_id"]
        ).assign(
                days_to_trending = np.where(random_days_to_trending < 0, 0, random_days_to_trending)
        )
    else:
        random_trending_class = np.random.randint(3, size=len(test))
        sample = test.filter(
                items=["video_id"]
        ).assign(
                trending_class = np.where(
                    random_trending_class == 0,
                    "early", 
                    np.where(
                        random_trending_class == 1,
                        "normal",
                        "late"
                    )
                )
        )

    return train, display_test, solution, sample

reg_train, reg_display_test, reg_solution, reg_sample = kaggle_split(videos_sel, True)
class_train, class_display_test, class_solution, class_sample = kaggle_split(videos_sel, False)

reg_train.to_csv("../docs/youtube_regression_train.csv", index=False)
reg_display_test.to_csv("../docs/youtube_regression_test.csv", index=False)
reg_solution.to_csv("../docs/youtube_regression_solution.csv", index=False)
reg_sample.to_csv("../docs/youtube_regression_sample.csv", index=False)

class_train.to_csv("../docs/youtube_classification_train.csv", index=False)
class_display_test.to_csv("../docs/youtube_classification_test.csv", index=False)
class_solution.to_csv("../docs/youtube_classification_solution.csv", index=False)
class_sample.to_csv("../docs/youtube_classification_sample.csv", index=False)
