package com.estudo;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

public class HelloWorldHandler implements RequestHandler<Object, HelloWorldHandler.RespostaJson> {
    public record RespostaJson(int statusCode, String body) {
    }

    @Override
    public RespostaJson handleRequest(Object s, Context context) {
        return new RespostaJson(200, "Hellow Terraform!");
    }

}