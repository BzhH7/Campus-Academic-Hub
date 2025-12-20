package com.bzh.nwpusurvivalmanual.controller;

import com.bzh.nwpusurvivalmanual.entity.CommentManager;
import com.bzh.nwpusurvivalmanual.entity.CommentUser;
import com.bzh.nwpusurvivalmanual.mapper.CommentMapper;
import com.bzh.nwpusurvivalmanual.model.comment;
import com.bzh.nwpusurvivalmanual.model.Course;
import com.bzh.nwpusurvivalmanual.service.CommentService;
import com.bzh.nwpusurvivalmanual.utils.response.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class CommentController {

    private final CommentService commentService;

    @Autowired
    private CommentMapper commentMapper;

    @Autowired
    public CommentController(CommentService commentService){
        this.commentService = commentService;
    }

    @GetMapping("/comment/course/visible")
    public Result getCourseComments(@RequestParam String cno) {
        try {
            List<comment> list = commentMapper.selectVisibleCommentsByCno(cno);
            return Result.success(list);
        } catch (Exception e) {
            return Result.fail(null, 500, "获取评论失败");
        }
    }

    @RequestMapping(value = "/comment/all", method = RequestMethod.GET)
    @ResponseBody
    public Result getAllCommentInfo(){
        List<comment> data;
        data = commentService.selectAll();

        return Result.success(data);
    }

    @RequestMapping(value = "/comment/limit/all", method = RequestMethod.GET)
    @ResponseBody
    public Result getAllCommentInfoRegional(@RequestParam(value = "start", defaultValue = "")String start,
                                            @RequestParam(value = "offset", defaultValue = "")String offset){
        List<comment> data;
        try {
            int a = Integer.parseInt(start);
            int b = Integer.parseInt(offset);
            data = this.commentService.selectAllRegional(a,b);
            return Result.success(data);
        }catch (Exception e){
            return Result.fail(e.getMessage(), 404, "select error");
        }
    }

    @RequestMapping(value = "/comment/user", method = RequestMethod.GET)
    @ResponseBody
    public Result getAllCommentInfoUser(){
        List<CommentUser> data;
        data = commentService.selectAllUser();

        return Result.success(data);
    }
    @RequestMapping(value = "/comment/limit/user", method = RequestMethod.GET)
    @ResponseBody
    public Result getAllCommentInfoUserRegional(@RequestParam(value = "start", defaultValue = "")String start,
                                            @RequestParam(value = "offset", defaultValue = "")String offset){
        List<CommentUser> data;
        try {
            int a = Integer.parseInt(start);
            int b = Integer.parseInt(offset);
            data = this.commentService.selectAllUserRegional(a,b);
            return Result.success(data);
        }catch (Exception e){
            return Result.fail(e.getMessage(), 404, "select error");
        }
    }
    @RequestMapping(value = "/comment/manager", method = RequestMethod.GET)
    @ResponseBody
    public Result getAllCommentInfoManager(){
        List<CommentManager> data;
        data = commentService.selectAllManager();

        return Result.success(data);
    }

    @RequestMapping(value = "/comment/limit/manager", method = RequestMethod.GET)
    @ResponseBody
    public Result getAllCommentInfoManagerRegional(@RequestParam(value = "start", defaultValue = "")String start,
                                            @RequestParam(value = "offset", defaultValue = "")String offset){
        List<CommentManager> data;
        try {
            int a = Integer.parseInt(start);
            int b = Integer.parseInt(offset);
            data = this.commentService.selectAllManagerRegional(a,b);
            return Result.success(data);
        }catch (Exception e){
            return Result.fail(e.getMessage(), 404, "select error");
        }
    }

    @RequestMapping(value = "/comment/number", method = RequestMethod.GET)
    @ResponseBody
    public Result selectCommentNum(){

        try {
            int data = this.commentService.selectCommentNum();
            return Result.success(data);
        }catch (Exception e){
            return Result.fail(e.getMessage(), 404, "select error");
        }

    }

    @RequestMapping(value = "/comment/new", method = RequestMethod.POST)
    @ResponseBody
    public Result insertComment(@RequestBody comment comment){
        try {
            this.commentService.insertComment(comment);
            return Result.success(null);
        }catch (Exception e){
            return Result.fail(null, 114, e.getMessage());
        }
    }

    @RequestMapping(value = "/comment/delete", method = RequestMethod.POST)
    @ResponseBody
    public Result deleteByKey(@RequestBody comment comment){
        try {

            this.commentService.deleteByKey(comment.getCno(), comment.getCid());
            return Result.success(null);
        }catch (Exception e){
            return Result.fail(null, 116, e.getMessage());
        }
    }

    @RequestMapping(value = "/course/comment/num", method = RequestMethod.GET)
    @ResponseBody
    public Result getCommentNumByCno(@RequestParam(value = "cno", defaultValue = "") String cno){
        try {
            int data = this.commentService.getCommentNumByCno(cno);
            return Result.success(data);
        }catch (Exception e){
            return Result.fail(null,118,e.getMessage());
        }
    }


    @RequestMapping(value = "/comment/pass", method = RequestMethod.POST)
    @ResponseBody
    public Result passComment(@RequestBody comment comment){
        try {
            int num = this.commentService.passComment(comment.getCno(), comment.getCid());
            return Result.success(num);
        }catch (Exception e){
            return Result.fail(null, 155, e.getMessage());
        }
    }
}
