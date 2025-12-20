package com.bzh.nwpusurvivalmanual.entity;

import java.sql.Timestamp;

public class ForumPost {
    private int id;
    private String title;
    private String content;
    private String author;
    private String tag;
    private Timestamp create_time;
    private int view_count;

    // Getters and Setters (可以使用 Lombok @Data, 如果没装就手动生成)
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }
    public String getTag() { return tag; }
    public void setTag(String tag) { this.tag = tag; }
    public Timestamp getCreate_time() { return create_time; }
    public void setCreate_time(Timestamp create_time) { this.create_time = create_time; }
    public int getView_count() { return view_count; }
    public void setView_count(int view_count) { this.view_count = view_count; }
}