package com.example.push_book;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.content.Intent;

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