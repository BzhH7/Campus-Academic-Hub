// src/main/java/com/bzh/nwpusurvivalmanual/entity/ForumReply.java
package com.bzh.nwpusurvivalmanual.entity;

import lombok.Data;

@Data
public class ForumReply {
    private int id;
    private int post_id;
    private String content;
    private String author;
    private String create_time;
}