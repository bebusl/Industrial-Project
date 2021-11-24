package com.example.push_book;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;

import com.example.push_book.ui.login.LoginActivity;
import android.content.Intent;

public class sing_in extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sing_in);
    }
    public void onClick(View view){
        Intent intent = new Intent(this, LoginActivity.class);
        startActivity(intent);
    }
}