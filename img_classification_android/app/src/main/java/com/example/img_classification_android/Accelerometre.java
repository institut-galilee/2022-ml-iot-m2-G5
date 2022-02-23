package com.example.img_classification_android;


import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import androidx.appcompat.app.AppCompatActivity;

import com.example.img_classification_android.cnn.impl.CNNExtractorServiceImpl;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;



public class Accelerometre implements SensorEventListener {

    private static final String TAG = "accelerometre";
    int[] Vals = new int[3];
    private int avertissement;
    private double vitesse;
    public String message;
    public String label;


    public void AccelerometerInit(Context context) {

        SensorManager sm = (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
        Sensor accelerometer = sm.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        sm.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_NORMAL);

    }

    public double getVitesse()
    {
        return this.vitesse;
    }
    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        Accelerometre.send sendcode = new Accelerometre.send();
        // le bruit : la somme des vitesses au repos
        double bruits = 0;
        //approximation_bruit : il s'agit de la moyenne des vitesses au repos pour approximer le bruit
        //on initialise le bruit a 0,4 car sa moyenne tend vers cette valeur
        double approximation_bruit = 0.4;
        //compteur du nombre de bruits enregistrés
        //commence a 1 car on initialise à 0.4
        int cpt = 1;
        //affichage des valeurs
        /*Log.d(TAG, "onSensorChanged: X:" + sensorEvent.values[0] + " | Y: " + sensorEvent.values[1] + " | Z: " + sensorEvent.values[2]);*/

        // l'équation de la vitesse = SQRT(x*x + y*y + z*z). En utilisant ceci, quand le téléphone est au repos la vitesse sera celle de la pesanteur - 9.8 m/s.
        double pesanteur = Math.sqrt(Math.pow(sensorEvent.values[0], 2)+ Math.pow(sensorEvent.values[1], 2) + Math.pow(sensorEvent.values[2], 2));
        //si on soustrait la pesanteur avec SensorManager.GRAVITY_EARTH, on obtient 0 m/s
        // comme il y a du bruit qui provoque un décalage de 0,4 m/s, cela veut dire que lorsque la vitesse est dans
        // l'intervalle [0;0,4] alors l'appareil est considéré etre en repos
        vitesse = Math.abs(pesanteur - SensorManager.GRAVITY_EARTH);

        message = Double.toString(vitesse);




        //Log.i(TAG, "getPredictedLabel: " + this.label);
        //Log.d(TAG, message);
        sendcode.execute();
    }

    //partie connexion

    class send extends AsyncTask<Void,Void,Void> {
        Socket s;
        PrintWriter pw;
        PrintWriter pw2;
        @Override
        protected Void doInBackground(Void...params){
            try {
                s = new Socket("192.168.1.29",8000);



                pw = new PrintWriter(s.getOutputStream(), true);
                //Log.d(TAG, "message1111 : " + message);
                pw.write(message);
                pw.flush();
                pw.close();
                s.close();

            } catch (UnknownHostException e) {
                System.out.println("Fail1");
                e.printStackTrace();
            } catch (IOException e) {
                System.out.println("Fail2");
                e.printStackTrace();
            }
            return null;
        }
    }
}