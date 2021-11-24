package com.example.push_book;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class mypage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_mypage);
    }
    public void Click1(View view){
        Intent intent = new Intent(this, wish_list.class);
        startActivity(intent);
    }
    public void Click2(View view){
        Intent intent = new Intent(this, search_list.class);
        startActivity(intent);
    }
}