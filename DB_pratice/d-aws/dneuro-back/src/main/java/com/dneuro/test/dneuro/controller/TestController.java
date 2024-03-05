package com.dneuro.test.dneuro.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    @GetMapping("/helloworld")
    public String test() {
        return "Do you want to build a Snowman?";
    }

}