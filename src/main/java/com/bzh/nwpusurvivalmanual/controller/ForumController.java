package com.bzh.nwpusurvivalmanual.controller;
import com.bzh.nwpusurvivalmanual.entity.ForumPost;
import com.bzh.nwpusurvivalmanual.mapper.ForumMapper;
import com.bzh.nwpusurvivalmanual.utils.response.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/forum")
public class ForumController {

    @Autowired
    private ForumMapper forumMapper;

    // 获取帖子列表
    @GetMapping("/all")
    public Result getAllPosts() {
        try {
            List<ForumPost> posts = forumMapper.getAllPosts();
            return Result.success(posts);
        } catch (Exception e) {
            return Result.fail(null, 500, "获取失败");
        }
    }

    // 发布帖子
    @PostMapping("/add")
    public Result addPost(@RequestBody ForumPost post) {
        try {
            forumMapper.insertPost(post);
            return Result.success("发布成功");
        } catch (Exception e) {
            return Result.fail(null, 500, "发布失败: " + e.getMessage());
        }
    }
}