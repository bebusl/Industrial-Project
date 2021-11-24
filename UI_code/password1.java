package com.example.push_book;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.content.Intent;
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
