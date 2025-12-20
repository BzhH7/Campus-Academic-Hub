package com.bzh.nwpusurvivalmanual.mapper;

import com.bzh.nwpusurvivalmanual.entity.ForumPost;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface ForumMapper {
    // 获取所有帖子，按时间倒序
    @Select("SELECT * FROM forum_post ORDER BY create_time DESC")
    List<ForumPost> getAllPosts();

    // 发布新帖子
    @Insert("INSERT INTO forum_post(title, content, author, tag) VALUES(#{title}, #{content}, #{author}, #{tag})")
    int insertPost(ForumPost post);
}