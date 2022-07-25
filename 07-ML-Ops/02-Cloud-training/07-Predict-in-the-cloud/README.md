
[//]: # ( challenge tech stack: compute-engine gcloud )

**💻 Install the package of the current challenge with `make reinstall_package`**

**💻 Do not forget to handle your `.env` file (_copy_ the `.env.sample`, _fill_ the `.env`, _allow_ `direnv`)**

[//]: # ( challenge instructions )

Ever been stranded on a spot with low connectivity but still want to work on your data science project?

Use your vm! You only need limited bandwidth to communicate with the vm, but you will still benefit from the high bandwith from the vm to rest of the Internet when you use it...

Now that you have setup your vm for the WagonCab project, it is ready for you anytime! You can switch it on and off in a breathe to work on your project.

Let's say a customer wants to estimate the cost of a ride for 3 persons on March 4th, 2015 at 5:33PM from 40.7812198,-73.9709985 to 40.6412948,-73.7802589.

**❓ How do you make a prediction with your vm ?**

Start your vm and make a prediction for the customer with your latest trained model.

Store the result in `~/code/<user.github_nickname>/{{local_path_to("07-ML-Ops/02-Cloud-training/07-Predict-in-the-cloud")}}/model/tests/cloud_prediction/pred.txt`

**💻 Predict the cost of the ride and store it in the `pred.txt` file**

**🧪 Run the tests with `make dev_test`**

👉 `test_cloud_prediction_pred` should be ✅

🏁 Congrats!
