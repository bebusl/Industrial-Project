package com.example.push_book;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.content.Intent;
import org.json.JSONException;
import java.io.IOException;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final api at = new api();
        Executors.newSingleThreadExecutor().execute(new Runnable() {
            @Override
            public void run () {
                try {
                    at.func();
                } catch (IOException | JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }
    public void onClick(View view){
        Intent intent = new Intent(this, keyword.class);
        startActivity(intent);
    }
}