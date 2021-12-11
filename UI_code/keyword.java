package com.example.book_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class keyword extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_keyword);
    }
    public void onClick(View view){
        Intent intent = new Intent(this, result.class);
        startActivity(intent);
    }

}
