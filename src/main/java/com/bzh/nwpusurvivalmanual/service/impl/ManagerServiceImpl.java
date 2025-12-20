package com.bzh.nwpusurvivalmanual.service.impl;

import com.bzh.nwpusurvivalmanual.mapper.ManagerMapper;
import com.bzh.nwpusurvivalmanual.model.Manager;
import com.bzh.nwpusurvivalmanual.service.ManagerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ManagerServiceImpl implements ManagerService {

    private ManagerMapper managerMapper;

    @Autowired
    public ManagerServiceImpl(ManagerMapper managerMapper){
        this.managerMapper = managerMapper;
    }

    @Override
    public List<Manager> selectAll(){
        return managerMapper.selectAll();
    }
}
