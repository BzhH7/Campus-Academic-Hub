package com.bzh.nwpusurvivalmanual.mapper;

import com.bzh.nwpusurvivalmanual.entity.ForumPost;
import com.bzh.nwpusurvivalmanual.entity.ForumReply;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface ForumMapper {

    @Select("SELECT * FROM forum_post ORDER BY create_time DESC")
    List<ForumPost> getAllPosts();

    @Insert("INSERT INTO forum_post(title, content, author, tag, create_time, view_count) " +
            "VALUES(#{title}, #{content}, #{author}, #{tag}, NOW(), 0)")
    int insertPost(ForumPost post);

    @Select("SELECT * FROM forum_post WHERE id = #{id}")
    ForumPost getPostById(@Param("id") int id);

    @Select("SELECT * FROM forum_reply WHERE post_id = #{postId} ORDER BY create_time ASC")
    List<ForumReply> getRepliesByPostId(@Param("postId") int postId);

    @Insert("INSERT INTO forum_reply(post_id, content, author, create_time) VALUES(#{post_id}, #{content}, #{author}, NOW())")
    int insertReply(ForumReply reply);

    @Update("UPDATE forum_post SET view_count = view_count + 1 WHERE id = #{id}")
    void incrementViewCount(@Param("id") int id);

    // 【新增】删除帖子下的回复
    @Delete("DELETE FROM forum_reply WHERE post_id = #{postId}")
    void deleteRepliesByPostId(@Param("postId") int postId);

    // 【新增】删除帖子本体
    @Delete("DELETE FROM forum_post WHERE id = #{id}")
    int deletePostById(@Param("id") int id);
}