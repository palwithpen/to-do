"use client";

import React, { useState, useEffect } from "react";
import {
  Container,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Checkbox,
  IconButton,
  TextField,
  Button,
  Paper,
  TableContainer,
} from "@mui/material";
import { Edit, Delete, Save, Add, Cancel } from "@mui/icons-material";
import Styles from "./page.module.css";
import { call } from "../utility/api";
import {jwtDecode} from 'jwt-decode';
import { useRouter } from 'next/navigation';

const TodoList = () => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ name: "", description: "" });
  const [token, setToken] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    if (storedToken) {
      setToken(storedToken);
      console.log(token)
    } else {
      router.push("/login");
    }
  }, [router]);

  useEffect(() => {
    if (token) {
      validateToken(token);

      async function fetchTasks() {
        try {
          const response = await call("GET", "http://localhost:8000/tasks/", { Authorization: `Bearer ${token}` });
          const data = await response;
          const formattedTasks = data.map((task) => ({
            id: task.id,
            name: task.title,
            description: task.description,
            status: task.status,
            isEditing: false,
            original: { ...task }
          }));
          setTasks(formattedTasks);
        } catch (error) {
          console.error("Error fetching tasks:", error);
        }
      }
      fetchTasks();
    }
  }, [token]);

  const validateToken = (token) => {
    try {
      const decoded = jwtDecode(token);
      const currentTime = Date.now() / 1000;
      if (decoded.exp < currentTime) {
        router.push("/login");
      }
    } catch (error) {
      console.error("Token validation failed:", error);
      router.push("/login");
    }
  };

  const handleCheckboxChange = (id) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === id ? { ...task, status: !task.status } : task
      )
    );
  };

  const handleEditClick = (id) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === id ? { ...task, isEditing: true } : task
      )
    );
  };

  const handleCancelClick = (id) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === id
          ? {
              ...task,
              isEditing: false,
              name: task.original.title,
              description: task.original.description,
            }
          : task
      )
    );
  };

  const handleSaveClick = async (id) => {
    const updatedTask = tasks.find((task) => task.id === id);
    try {
      await call("PUT", `http://localhost:8000/tasks/${id}`, { Authorization: `Bearer ${token}` }, {
        title: updatedTask.name,
        description: updatedTask.description,
        status: updatedTask.status,
        id: updatedTask.id
      });
      setTasks((prevTasks) =>
        prevTasks.map((task) =>
          task.id === id ? { ...task, isEditing: false } : task
        )
      );
    } catch (error) {
      console.error("Error saving task:", error);
    }
  };

  const handleDeleteClick = async (id) => {
    try {
      const response = await call("DELETE", `http://localhost:8000/tasks/${id}`, { Authorization: `Bearer ${token}` });
      if (response.statusCode === 200) {
        setTasks((prevTasks) => prevTasks.filter((task) => task.id !== id));
      }
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  const handleInputChange = (e, id) => {
    const { name, value } = e.target;
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === id ? { ...task, [name]: value } : task
      )
    );
  };

  const handleNewTaskChange = (e) => {
    const { name, value } = e.target;
    setNewTask({ ...newTask, [name]: value });
  };

  const handleAddTask = async () => {
    try {
      const response = await call("POST", "http://localhost:8000/tasks/", { Authorization: `Bearer ${token}` }, {
        title: newTask.name,
        description: newTask.description,
        status: false,
      });
      if (response.statusCode === 200) {
        setTasks((prevTasks) => [
          ...prevTasks,
          {
            id: response.data.id,
            name: newTask.name,
            description: newTask.description,
            status: false,
            isEditing: false,
            original: {
              title: newTask.name,
              description: newTask.description,
              status: false
            }
          },
        ]);
        setNewTask({ name: "", description: "" });
      } else {
        alert("Unable to add tasks");
      }
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };

  return (
    <Container className={Styles.mainContainer}>
      <br/>
      <TableContainer
        component={Paper}
        style={{ maxHeight: 400, overflow: "auto" }}
      >
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Task Name</TableCell>
              <TableCell>Task Description</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks.map((task) => (
              <TableRow key={task.id}>
                <TableCell>
                  {task.isEditing ? (
                    <TextField
                      value={task.name}
                      name="name"
                      onChange={(e) => handleInputChange(e, task.id)}
                      fullWidth
                    />
                  ) : (
                    task.name
                  )}
                </TableCell>
                <TableCell>
                  {task.isEditing ? (
                    <TextField
                      value={task.description}
                      name="description"
                      onChange={(e) => handleInputChange(e, task.id)}
                      fullWidth
                    />
                  ) : (
                    task.description
                  )}
                </TableCell>
                <TableCell>
                  <Checkbox
                    checked={task.status}
                    onChange={() => handleCheckboxChange(task.id)}
                  />
                </TableCell>
                <TableCell>
                  {task.isEditing ? (
                    <>
                      <IconButton onClick={() => handleSaveClick(task.id)}>
                        <Save />
                      </IconButton>
                      <IconButton onClick={() => handleCancelClick(task.id)}>
                        <Cancel />
                      </IconButton>
                    </>
                  ) : (
                    <>
                      <IconButton onClick={() => handleEditClick(task.id)}>
                        <Edit />
                      </IconButton>
                      <IconButton onClick={() => handleDeleteClick(task.id)}>
                        <Delete />
                      </IconButton>
                    </>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <div style={{ marginTop: "20px" }}>
        <TextField
          label="New Task Name"
          value={newTask.name}
          name="name"
          onChange={handleNewTaskChange}
          style={{ marginRight: "10px" }}
        />
        <TextField
          label="New Task Description"
          value={newTask.description}
          name="description"
          onChange={handleNewTaskChange}
          style={{ marginRight: "10px" }}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleAddTask}
          startIcon={<Add />}
        >
          Add Task
        </Button>
      </div>
    </Container>
  );
};

export default TodoList;
