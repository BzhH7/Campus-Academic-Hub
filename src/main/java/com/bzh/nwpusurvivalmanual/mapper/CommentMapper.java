package com.bzh.nwpusurvivalmanual.mapper;

import com.bzh.nwpusurvivalmanual.entity.CommentManager;
import com.bzh.nwpusurvivalmanual.entity.CommentUser;
import com.bzh.nwpusurvivalmanual.model.Course;
import com.bzh.nwpusurvivalmanual.model.comment;
import org.apache.ibatis.annotations.*;

import java.util.List;

/**
 * 实现数据库中comment表与comment类的映射
 *
 * @author Yuanhong YU
 * @see comment
 * @version 1.0
 */

@Mapper
public interface CommentMapper {

    @Select("SELECT * FROM comment")

    List<comment>selectAll();

    @Select("SELECT * FROM comment_user")
    List<CommentUser>selectAllUser();

    @Select("SELECT * FROM comment_manager")
    List<CommentManager>selectAllManager();

    @Select("SELECT * FROM comment limit #{start},#{offset}")
    List<comment>selectAllRegional(@Param("start")int start, @Param("offset")int offset);

    @Select("SELECT * FROM comment_user limit #{start},#{offset}")
    List<CommentUser>selectAllUserRegional(@Param("start")int start, @Param("offset")int offset);

    @Select("SELECT c.cno, co.cname, c.cid, c.time, c.detail, c.visible, c.isselect, c.sscore " +
            "FROM comment c " +
            "LEFT JOIN course co ON c.cno = co.cno " +
            "ORDER BY c.time DESC " +  // 按时间倒序，新评论在前面
            "LIMIT #{start}, #{offset}")
    List<CommentManager> selectAllManagerRegional(@Param("start")int start, @Param("offset")int offset);

    @Select("SELECT * FROM comment WHERE cno = #{cno} AND visible = 1 ORDER BY STR_TO_DATE(time, '%Y/%m/%d') DESC")
    List<comment> selectVisibleCommentsByCno(@Param("cno") String cno);

    @Select("SELECT COUNT(*) FROM comment")
    int selectCommentNum();

    @Insert("INSERT INTO comment VALUES(#{cno},#{cid},#{sno},#{time},#{detail},#{isselect},#{sscore}," +
            "#{visible})")
    int insertComment(comment comment);

    @Delete("DELETE FROM comment WHERE cno=#{cno} and cid=#{cid}")
    int deleteByKey(@Param("cno")String cno, @Param("cid")int cid);

    @Select("SELECT COUNT(*) FROM comment WHERE cno=#{cno}")
    int getCommentNumByCno(@Param("cno")String cno);


    @Update("UPDATE comment SET visible=1 WHERE cno=#{cno} and cid=#{cid}")
    int passComment(@Param("cno")String cno, @Param("cid")int cid);
}
