package com.example.book_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class my_page extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_page);
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
