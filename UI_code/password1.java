package com.example.book_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class password1 extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_password1);
    }
    public void onClick(View view){
        Intent intent = new Intent(this, password2.class);
        startActivity(intent);

        finish();
    }

}
