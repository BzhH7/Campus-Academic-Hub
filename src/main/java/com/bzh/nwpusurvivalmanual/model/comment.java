package com.bzh.nwpusurvivalmanual.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class comment {
    private String cno;

    private int cid;

    private String sno;

    private String time;

    private String detail;

    private int isselect;

    private float sscore;

    private int visible;
}
