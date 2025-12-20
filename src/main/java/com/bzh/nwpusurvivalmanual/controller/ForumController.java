package com.bzh.nwpusurvivalmanual.controller;

import com.bzh.nwpusurvivalmanual.entity.ForumPost;
import com.bzh.nwpusurvivalmanual.entity.ForumReply;
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

    @GetMapping("/all")
    public Result getAllPosts() {
        try {
            List<ForumPost> posts = forumMapper.getAllPosts();
            return Result.success(posts);
        } catch (Exception e) {
            return Result.fail(null, 500, "获取失败");
        }
    }

    @PostMapping("/add")
    public Result addPost(@RequestBody ForumPost post) {
        try {
            forumMapper.insertPost(post);
            return Result.success("发布成功");
        } catch (Exception e) {
            return Result.fail(null, 500, "发布失败: " + e.getMessage());
        }
    }

    @GetMapping("/detail")
    public Result getPostDetail(@RequestParam int id) {
        try {
            forumMapper.incrementViewCount(id);
            ForumPost post = forumMapper.getPostById(id);
            if (post == null) return Result.fail(null, 404, "帖子不存在");
            return Result.success(post);
        } catch (Exception e) {
            return Result.fail(null, 500, e.getMessage());
        }
    }

    @GetMapping("/replies")
    public Result getReplies(@RequestParam int postId) {
        return Result.success(forumMapper.getRepliesByPostId(postId));
    }

    @PostMapping("/reply/add")
    public Result addReply(@RequestBody ForumReply reply) {
        try {
            forumMapper.insertReply(reply);
            return Result.success("回复成功");
        } catch (Exception e) {
            return Result.fail(null, 500, "回复失败");
        }
    }

    // 【新增】删除帖子接口
    @PostMapping("/delete")
    public Result deletePost(@RequestBody ForumPost post) {
        try {
            // 先删回复，再删帖子，保持数据干净
            forumMapper.deleteRepliesByPostId(post.getId());
            forumMapper.deletePostById(post.getId());
            return Result.success("删除成功");
        } catch (Exception e) {
            return Result.fail(null, 500, "删除失败: " + e.getMessage());
        }
    }
}