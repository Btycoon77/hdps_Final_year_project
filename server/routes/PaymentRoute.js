const {
  initializeKhaltiPayment,
  verifyKhaltiPayment,
} = require("../controllers/khalti");

const Payment = require("../models/PaymentModel");
const PurchaseItemModel = require("../models/PurchaseItemtModel");
const Item = require("../models/ItemModel");

const express = require("express");

const paymentRouter = express.Router();

paymentRouter.get("/initialize-khalti", async (req, res) => {
  try {
    //try catch for error handling
    const { itemId, totalPrice, website_url } = req.body;
    const itemData = await Item.findOne({
      _id: itemId,
      price: Number(totalPrice),
    });

    if (!itemData) {
      return res.status(400).send({
        success: false,
        message: "item not found",
      });
    }
    // creating a purchase document to store purchase info
    const purchasedItemData = await PurchasedItemModel.create({
      item: itemId,
      paymentMethod: "khalti",
      totalPrice: totalPrice * 100,
    });

    const paymentInitate = await initializeKhaltiPayment({
      amount: totalPrice * 100, // amount should be in paisa (Rs * 100)
      purchase_order_id: purchasedItemData._id, // purchase_order_id because we need to verify it later
      purchase_order_name: itemData.name,
      return_url: `${process.env.BACKEND_URI}/complete-khalti-payment`, // it can be even managed from frontedn
      website_url,
    });

    res.json({
      success: true,
      purchasedItemData,
      payment: paymentInitate,
    });
  } catch (error) {
    res.json({
      success: false,
      error,
    });
  }
});

// it is our `return url` where we verify the payment done by user
paymentRouter.get("/complete-khalti-payment", async (req, res) => {
  const {
    pidx,
    txnId,
    amount,
    mobile,
    purchase_order_id,
    purchase_order_name,
    transaction_id,
  } = req.query;

  try {
    const paymentInfo = await verifyKhaltiPayment(pidx);

    // Check if payment is completed and details match
    if (
      paymentInfo?.status !== "Completed" ||
      paymentInfo.transaction_id !== transaction_id ||
      Number(paymentInfo.total_amount) !== Number(amount)
    ) {
      return res.status(400).json({
        success: false,
        message: "Incomplete information",
        paymentInfo,
      });
    }

    // Check if payment done in valid item
    const purchasedItemData = await PurchasedItem.find({
      _id: purchase_order_id,
      totalPrice: amount,
    });

    if (!purchasedItemData) {
      return res.status(400).send({
        success: false,
        message: "Purchased data not found",
      });
    }
    // updating purchase record
    await PurchasedItem.findByIdAndUpdate(
      purchase_order_id,

      {
        $set: {
          status: "completed",
        },
      }
    );

    // Create a new payment record
    const paymentData = await Payment.create({
      pidx,
      transactionId: transaction_id,
      productId: purchase_order_id,
      amount,
      dataFromVerificationReq: paymentInfo,
      apiQueryFromUser: req.query,
      paymentGateway: "khalti",
      status: "success",
    });

    // Send success response
    res.json({
      success: true,
      message: "Payment Successful",
      paymentData,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({
      success: false,
      message: "An error occurred",
      error,
    });
  }
});

module.exports = paymentRouter;