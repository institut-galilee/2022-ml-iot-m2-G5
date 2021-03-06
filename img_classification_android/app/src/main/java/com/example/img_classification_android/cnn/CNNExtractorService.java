package com.example.img_classification_android.cnn;

import org.opencv.core.Mat;
import org.opencv.dnn.Net;

public interface CNNExtractorService {

    Net getConvertedNet(String clsModelPath, String tag);

    String getPredictedLabel(Mat inputImage, Net dnnNet, String classesPath);
}