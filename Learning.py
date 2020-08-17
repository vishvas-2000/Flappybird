num_episodes = 100
target_net_update_iter = 5
beta = 0.95
tf.autograph.set_verbosity(0)

rewards = []
rewards_avg =[]

fig = plot.figure(figsize=(9,3))
ax = fig.add_subplot(111)
ax.set_xlabel("Episodes")
ax.set_ylabel("Rewards")
fig.show()
show_in_every = 1
for episode in range(num_episodes):
    state =env.reset()
    state = np.array(state)/ 50
    
    terminated = False
    reward_episode = 0
    agent.epsilon = agent.get_exploration_rate(episode)
    time = 0
    while not terminated:
#         env.render()
        if episode % show_in_every == 0:
            env.render()
        
        action = agent.act(state)
        next_state, reward, terminated, info = agent.env.step(action)
        next_state = tf.convert_to_tensor(np.array(next_state)/50)
        agent.store(state, action, reward, next_state, terminated)
        state = next_state
        reward_episode += reward
        time +=1
        if time >= 2000:
            break
  
    if len(agent.experience) > agent.batch_size:
            agent.train()
    
    if episode % target_net_update_iter == 0:
            agent.update_target_net()
    
    rewards.append(reward_episode) 
    if episode == 0:
        rewards_avg.append(reward_episode)
    else:
        rewards_avg.append((1 -np.power((1-beta),episode)) * (beta * (rewards_avg[-1]) + (1 - beta) * reward_episode))
    
    ax.plot(rewards, 'r')
    ax.plot(rewards_avg, 'b')
    ax.set_xlim(left= max(0,episode-50), right= episode+20)
    fig.canvas.draw()
    